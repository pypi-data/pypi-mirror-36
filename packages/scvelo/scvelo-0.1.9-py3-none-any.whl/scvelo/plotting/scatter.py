from .utils import interpret_colorkey, get_components, plot_colorbar, savefig
from .docs import doc_scatter, doc_params
import matplotlib.pyplot as pl
import scanpy.api.pl as scpl
from matplotlib.ticker import MaxNLocator


@doc_params(scatter=doc_scatter)
def scatter(adata, x=None, y=None, basis=None, color=None, use_raw=None, layer=None, color_map=None, colorbar=False,
            palette=None, size=5, alpha=1, perc=None, sort_order=True, groups=None, components=None, projection='2d',
            legend_loc='none', legend_fontsize=None, legend_fontweight=None, right_margin=None, left_margin=None,
            xlabel=None, ylabel=None, title=None, fontsize=None, figsize=(7,5), dpi=100, frameon=False, show=True,
            save=None, ax=None, **kwargs):
    """\
    Scatter plot along observations or variables axes.

    Arguments
    ---------
    adata: :class:`~anndata.AnnData`
        Annotated data matrix.
    x: `str`, `np.ndarray` or `None` (default: `None`)
        x coordinate
    y: `str`, `np.ndarray` or `None` (default: `None`)
        y coordinate
    {scatter}

    Returns
    -------
        If `show==False` a `matplotlib.Axis`
    """
    if basis is None: basis = [key for key in ['pca', 'tsne', 'umap'] if 'X_' + key in adata.obsm.keys()][-1]
    colors = color if isinstance(color, (list, tuple)) else [color]
    layers = layer if isinstance(layer, (list, tuple)) else [layer]

    if len(colors) > 1:
        for i, gs in enumerate(pl.GridSpec(1, len(colors), pl.figure(None, (figsize[0]*len(colors), figsize[1]), dpi=dpi))):
            scatter(adata, basis=basis, layer=layer, color=color[i], xlabel=xlabel, ylabel=ylabel, color_map=color_map,
                    perc=perc, size=size, alpha=alpha, fontsize=fontsize, frameon=frameon, title=title, show=False,
                    colorbar=colorbar, components=components, figsize=figsize, dpi=dpi, save=None, ax=pl.subplot(gs),
                    use_raw=use_raw, sort_order=sort_order, groups=groups, projection=projection,
                    legend_loc=legend_loc, legend_fontsize=legend_fontsize, legend_fontweight=legend_fontweight,
                    palette=palette, right_margin=right_margin, left_margin=left_margin, **kwargs)
        if isinstance(save, str): savefig('' if basis is None else basis, dpi=dpi, save=save, show=show)
        if show: pl.show()
        else: return ax

    elif len(layers) > 1:
        for i, gs in enumerate(pl.GridSpec(1, len(layers), pl.figure(None, (figsize[0] * len(layers), figsize[1]), dpi=dpi))):
            scatter(adata, basis=basis, layer=layers[i], color=color, xlabel=xlabel, ylabel=ylabel, color_map=color_map,
                    perc=perc, size=size, alpha=alpha, fontsize=fontsize, frameon=frameon, title=title, show=False,
                    colorbar=colorbar, components=components, figsize=figsize, dpi=dpi, save=None, ax=pl.subplot(gs),
                    use_raw=use_raw, sort_order=sort_order, groups=groups, projection=projection,
                    legend_loc=legend_loc, legend_fontsize=legend_fontsize, legend_fontweight=legend_fontweight,
                    palette=palette, right_margin=right_margin, left_margin=left_margin, **kwargs)
        if isinstance(save, str): savefig('' if basis is None else basis, dpi=dpi, save=save, show=show)
        if show: pl.show()
        else: return ax

    else:
        if ax is None: ax = pl.figure(None, figsize, dpi=dpi).gca()
        if color_map is None:
            color_map = 'viridis_r' if isinstance(color, str) and (color == 'root' or color == 'end') else 'RdBu_r'
        if color is None:
            color = 'clusters' if 'clusters' in adata.obs.keys() else 'louvain' if 'louvain' in adata.obs.keys() else 'grey'
        is_embedding = (x is None) | (y is None)

        if isinstance(color, str) and color in adata.obs.keys() \
                and adata.obs[color].dtype.name == 'category' and is_embedding:

            ax = scpl.scatter(adata, color=color, use_raw=use_raw, sort_order=sort_order, alpha=alpha, basis=basis,
                              groups=groups, components=components, projection=projection, legend_loc=legend_loc,
                              legend_fontsize=legend_fontsize, legend_fontweight=legend_fontweight, color_map=color_map,
                              palette=palette, right_margin=right_margin, left_margin=left_margin, size=size,
                              title=title, frameon=frameon, show=False, save=None, ax=ax, **kwargs)

        else:
            if is_embedding:
                X_emb = adata.obsm['X_' + basis][:, get_components(components)]
                x, y = X_emb[:, 0], X_emb[:, 1]
                ax.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
            else:
                ax.xaxis.set_major_locator(MaxNLocator(nbins=3))
                ax.yaxis.set_major_locator(MaxNLocator(nbins=3))
                labelsize = int(fontsize * .75) if fontsize is not None else None
                ax.tick_params(axis='both', which='major', labelsize=labelsize)

            c = interpret_colorkey(adata, color, layer, perc)
            pl.scatter(x, y, c=c, cmap=color_map, s=size, alpha=alpha, zorder=0, **kwargs)

            if isinstance(xlabel, str) and isinstance(ylabel, str):
                pl.xlabel(xlabel, fontsize=fontsize)
                pl.ylabel(ylabel, fontsize=fontsize)
            elif basis is not None:
                component_name = ('DC' if basis == 'diffmap' else 'tSNE' if basis == 'tsne' else 'UMAP' if basis == 'umap'
                else 'PC' if basis == 'pca' else basis.replace('draw_graph_', '').upper() if 'draw_graph' in basis else basis)
                pl.xlabel(component_name + '1')
                pl.ylabel(component_name + '2')

            if isinstance(title, str): pl.title(title, fontsize=fontsize)
            elif isinstance(layer, str) and isinstance(color, str): pl.title(color + ' ' + layer, fontsize=fontsize)
            elif isinstance(color, str): pl.title(color, fontsize=fontsize)

            if not frameon: pl.axis('off')
            if colorbar and len(c) == adata.n_obs and c.dtype: plot_colorbar(ax)

        if isinstance(save, str): savefig('' if basis is None else basis, dpi=dpi, save=save, show=show)

        if show: pl.show()
        else: return ax