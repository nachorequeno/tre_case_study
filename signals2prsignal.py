import sys

import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from ParetoLib.Geometry.Zone import Zone
from numpy import mean


def overlay(zone: Zone, fig: Figure = None) -> Figure:
    '''
    Overlays the Zones on top of the time series (e.g., electricity consumption records).
    :param zone:
    :param fig:
    :return:
    '''
    if fig is None:
        # fig = plt.figure()
        fig, ax = plt.subplots()
    else:
        axes = fig.get_axes()
        ax = axes[0]

    b, bp = zone.bmin[0], zone.bmax[0]
    e, ep = zone.emin[0], zone.emax[0]
    d, dp = zone.dmin[0], zone.dmax[0]

    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    # p1 = (b, e)
    # p2 = (b, b + dp)
    # p3 = (ep - dp, ep)
    # p4 = (bp, ep)
    # p5 = (bp, bp + d)
    # p6 = (e - d, e)

    # Begin
    ax.vlines(x=b, ymin=ymin, ymax=ymax, color='g', linestyle='-')
    ax.vlines(x=bp, ymin=ymin, ymax=ymax, color='g', linestyle='--')

    # End
    ax.vlines(x=e, ymin=ymin, ymax=ymax, color='r', linestyle='-')
    ax.vlines(x=ep, ymin=ymin, ymax=ymax, color='r', linestyle='--')

    # Grey zones between begin and end
    ax.fill_betweenx(y=[ymin, ymax], x1=b, x2=e, facecolor='grey', alpha=0.25)
    ax.fill_betweenx(y=[ymin, ymax], x1=b, x2=b + dp, facecolor='grey', alpha=0.25)
    ax.fill_betweenx(y=[ymin, ymax], x1=bp, x2=ep, facecolor='grey', alpha=0.25)
    ax.fill_betweenx(y=[ymin, ymax], x1=bp, x2=bp + d, facecolor='grey', alpha=0.25)
    ax.fill_betweenx(y=[ymin, ymax], x1=ep - dp, x2=ep, facecolor='grey', alpha=0.25)
    ax.fill_betweenx(y=[ymin, ymax], x1=e - d, x2=e, facecolor='grey', alpha=0.25)

    return fig

def signals2prsignal_opt(output_signal: str, input_signals: list[str]) -> None:
    df_output_signal = pd.DataFrame()
    df_mean_signal = pd.DataFrame()
    df_stdev_signal = pd.DataFrame()

    df_mean_signal["signal"] = 0.0
    df_stdev_signal["signal"] = 0.0

    for i, input_signal in enumerate(input_signals, start=1):
        # Read CSV file
        df_input_signal = pd.read_csv(input_signal, names=["time", "signal"], index_col=0)
        # mean
        # mean_increment = df_input_signal - df_mean_signal
        mean_increment = df_input_signal.add(-df_mean_signal, fill_value=0)
        df_mean_signal = df_mean_signal.add(mean_increment/i, fill_value=0)
        # stdev
        # stdev_increment = df_input_signal - df_mean_signal
        # stdev_increment = df_input_signal.add(-df_mean_signal, fill_value=0)
        # df_stdev_signal = df_stdev_signal.add(mean_increment * stdev_increment, fill_value=0)
        stdev_increment = pow(mean_increment, 2) * (i - 1)/i
        df_stdev_signal = df_stdev_signal.add(stdev_increment, fill_value=0)

    n = len(input_signals)
    df_output_signal["mean"] = df_mean_signal["signal"]
    df_output_signal["stdev"] = np.sqrt(df_stdev_signal["signal"]/n)

    # print(f"Number of signals: {n}")
    # print(df_output_signal.head())

    # Dump to output file
    df_output_signal.to_csv(output_signal, header=False)

def signals2prsignal(output_signal: str, input_signals: list[str]) -> None:
    df_aggregated_signals = pd.DataFrame()

    i = 0
    for input_signal in input_signals:
        # Read CSV file
        df_input_signal = pd.read_csv(input_signal, names=["time", f"signal_{i}"], index_col=0)
        df_aggregated_signals = df_aggregated_signals.add(df_input_signal, fill_value=0)
        i = i + 1

    # print(f"Number of signals: {i}")
    # print(df_aggregated_signals.head())

    df_output_signal = pd.DataFrame()
    df_output_signal["mean"] = df_aggregated_signals.mean(axis=1)
    df_output_signal["stdev"] = df_aggregated_signals.std(axis=1, ddof=1)

    # Dump to output file
    df_output_signal.to_csv(output_signal, header=False)

def plot_prsignal(output_signal: str, input_signals: list[str], fig: Figure = None) -> Figure:
    '''
    Plots a probabilistic signal that summarizes several time series with 95% interval confidence.
    :param output_signal:
    :param input_signals:
    :param fig:
    :return:
    '''
    if fig is None:
        # fig = plt.figure()
        fig, ax = plt.subplots()
    else:
        axes = fig.get_axes()
        ax = axes[0]

    df_aggregated_signals = pd.DataFrame()

    i = 0
    max_mean_signal_value = 0.0
    for input_signal in input_signals:
        # Read CSV file
        df_input_signal = pd.read_csv(input_signal, names=["time", "signal"], index_col=0)
        df_input_signal["id"] = i
        # Extracting the maximum signal values for adjusting the plotting axis
        mean_signal_value = mean(df_input_signal["signal"])
        max_mean_signal_value = max(max_mean_signal_value, mean_signal_value)
        # Reseting index for multiple signal concatenation
        df_input_signal = df_input_signal.reset_index()
        df_aggregated_signals = pd.concat([df_aggregated_signals, df_input_signal])
        i = i + 1

    # print(f"Number of signals: {i}")
    # print(df_aggregated_signals)

    print(f"Pivot: {i}")
    signals_wide = df_aggregated_signals.pivot(index="id", columns="time", values="signal")
    print(signals_wide.head())

    sns.lineplot(data=df_aggregated_signals, x="time", y="signal", ax=ax)
    max_y = 2.75 if max_mean_signal_value < 2.75 else 7.0
    plt.ylim(0, max_y)
    plt.xlim(0, 48)
    if output_signal is not None:
        plt.savefig(fname=output_signal, format='svg')

    return plt.gcf()


def plot_zones(output_signal: str, zones: list[Zone]) -> None:
    f: Figure = plt.figure()
    ax1 = f.add_subplot(111)
    ax1.set_xlim(0, 48)
    ax1.set_ylim(0, 48)
    for zone in zones:
        zone.plot_2D(fig=f)

    if output_signal is not None:
        plt.savefig(fname=output_signal, format='svg')

    plt.show()

def plot_prsignal_with_zones(output_signal: str, input_signals: list[str], zones: list[Zone]):
    f = plot_prsignal(output_signal, input_signals)
    for zone in zones:
        f = overlay(zone, f)

    if output_signal is not None:
        plt.savefig(fname=output_signal, format='svg')

    plt.show()


if __name__ == '__main__':
    # output_signal = sys.argv[1]
    # input_signals = sys.argv[2:]
    output_signal = "/mnt/d/git_projects/papers/tre_case_study/day_0_360_user_1143/fdi50/days_*"
    input_signals = "/mnt/d/git_projects/papers/tre_case_study/tre/fdi50.txt"
    # signals2prsignal_opt(output_signal, input_signals)
    signals2prsignal(f"./csv/{output_signal}.csv", input_signals)
    plot_prsignal(f"./svg/{output_signal}.svg", input_signals)
