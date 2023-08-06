Fuzzy call graphs

`f` (maybe) calls `g` if `g.name` is in `f.body`

This gives false positives

```
python call_graph.py      \
  "${ABS_PATH_OF_MODULE}" \
  > module_callgraph.gv   \
&& dot \
  -Tpdf module_callgraph.gv \
  -o module_callgraph.pdf   \
&& open module_callgraph.pdf
```

(Where `dot` is from https://www.graphviz.org/documentation/)

(Standard python setup distribution boilerplate is a shame - why does it have to be at top leve of project?)
