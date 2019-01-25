from ..graph import plot

# TODO : pandas series as input
def chart(series):

    # print the chart
    print("\n" + plot(series[-120:], {'height': 20}))  # print the chart
