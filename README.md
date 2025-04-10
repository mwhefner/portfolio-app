# M. W. Hefner's Web Portfolio

I maintain this web app to showcase my research publications and educational technology projects in mathematics, statistics, and data science. **[You can find the portfolio here.](https://mathymattic.pythonanywhere.com/)**

This is a multi-page Python web application based on Plotly's [Dash Open Source framework.](https://dash.plotly.com/) [Nerdamer](https://nerdamer.com/) and [math.js](https://mathjs.org/) are used for symbolic computer algebra, and [p5.js](https://p5js.org/) is used for interactive web graphics.

This application is open source: see LICENSE for details. 

If you have feedback, questions, or are interested in collaborating or contributing, feel free to get in touch directly!

## Console cheat sheet

Some useful copypasta for the console. **Before you do anything with [conda,](https://anaconda.org/anaconda/conda) I encourage you first to see [their documentation.](https://docs.conda.io/projects/conda/en/stable/)**

To create an environment from a yaml::

```
conda env create -f environment.yml
```

Creating/updating an environment yaml:

```
conda env export --from-history > environment.yml
```

Use `python ./develop.py` to run a development server on your local host machine.
