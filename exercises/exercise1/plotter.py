def plotter(ax, **options):
    ax.set_title(options.get("title"), loc="left")
    ax.set_xlabel(options.get("xlabel",""),loc="left")
    ax.set_ylabel(options.get("ylabel",""), rotation=90, loc="top")
    ax.tick_params(options.get("tp_axis"), rotation=0)
    fig = ax.get_figure()
    fig.tight_layout()
    ax.legend().remove()
    fig.savefig(options.get("path"))
    return ax

def annotater(ax, arrow=True, **options):
    arrowprops = dict(arrowstyle = "->", linewidth = 3, connectionstyle = "arc3, rad=.3")
    if arrow== True:
        ax.annotate(options.get("text", ""), xy= options.get("xy"), arrowprops=arrowprops, xytext = (options.get("xy")[0]+.2, options.get("xy")[1]+options.get("xy")[1]*0.15))
    else:
        ax.annotate(options.get("text", ""), xy= options.get("xy"))
    return ax

def formatter(val,pos):
     return f'{int(val/1000)}K'
