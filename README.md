# Perspective-3-Point Problem

Educational repo to illustrate the ambiguity leading to 4 valid solutions of the Perspective-3-Point problem.

In order to generate the visualizations, simply install the package and run the following command:

```bash
poetry install
```

Then you can generate the visualizations by running the following command:

```bash
poetry run manim -pql p3p_ambiguity/scenes/p3p_ambiguity.py P3PAmbiguity
```

If you just want to generate the final frame, simply run

```bash
poetry run manim -pql p3p_ambiguity/scenes/p3p_ambiguity.py P3PAmbiguity -s
```

