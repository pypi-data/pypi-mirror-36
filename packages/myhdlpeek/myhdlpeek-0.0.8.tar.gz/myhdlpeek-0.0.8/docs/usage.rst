========
Usage
========

The following Jupyter notebooks will illustrate how to use myhdlpeek.
Unfortunately, the Github Notebook viewer doesn't render the waveform displays
so you'll have to download and run the notebooks locally or click on the static HTML
link to see what myhdlpeek can do.

* Simple multiplexer: `[Notebook] <https://github.com/xesscorp/myhdlpeek/blob/master/examples/peeker_simple_mux.ipynb>`_ `[HTML] <http://www.xess.com/static/media/pages/peeker_simple_mux.html>`_
* Hierarchical adder: `[Notebook] <https://github.com/xesscorp/myhdlpeek/blob/master/examples/peeker_hier_add.ipynb>`_ `[HTML] <http://www.xess.com/static/media/pages/peeker_hier_add.html>`_
* Other Peeker options: `[Notebook] <https://github.com/xesscorp/myhdlpeek/blob/master/examples/peeker_options.ipynb>`_ `[HTML] <http://www.xess.com/static/media/pages/peeker_options.html>`_
* Tabular display: `[Notebook] <https://github.com/xesscorp/myhdlpeek/blob/master/examples/peeker_tables.ipynb>`_ `[HTML] <http://www.xess.com/static/media/pages/peeker_tables.html>`_
* Convenience functions: `[Notebook] <https://github.com/xesscorp/myhdlpeek/blob/master/examples/peeker_convenience_functions.ipynb>`_ `[HTML] <http://www.xess.com/static/media/pages/peeker_convenience_functions.html>`_
* Trigger functions: `[Notebook] <https://github.com/xesscorp/myhdlpeek/blob/master/examples/peeker_triggers.ipynb>`_ `[HTML] <http://www.xess.com/static/media/pages/peeker_triggers.html>`_
* Peeker groups: `[Notebook] <https://github.com/xesscorp/myhdlpeek/blob/master/examples/peeker_groups.ipynb>`_ `[HTML] <http://www.xess.com/static/media/pages/peeker_groups.html>`_
* Pandas export: `[Notebook] <https://github.com/xesscorp/myhdlpeek/blob/master/examples/peeker_dataframe.ipynb>`_ `[HTML] <http://www.xess.com/static/media/pages/peeker_dataframe.html>`_

Also, by default myhdlpeek is set up to work with the newer JupyterLab.
If you want to use it in an older Jupyter notebook, then do the following::

    import myhdlpeek
    myhdlpeek.USE_JUPYTERLAB = False

