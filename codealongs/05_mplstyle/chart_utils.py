def horizontal_bar_option(ax, **options):
    
    #print(options)
    #print(options.get("title", "default title"))
    
    ax.set_title(options.get("title",""),
                loc="left", pad = 25)
    ax.set_xlabel(options.get("xlabel",""), loc="left")
    ax.set_ylabel("JOB CATEGORY", rotation=0)
    ax.yaxis.set_label_coords(-0.1,1)

    ax.legend().remove()
    ax.invert_yaxis()
    
    return ax

def save_fig_from_ax(ax, save_path):
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(save_path)

def thousand_formatter(val,axis):
    
    return f'{int(val/1000)}K'