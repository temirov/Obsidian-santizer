# import transitions

from transitions.extensions import GraphMachine
m = Model()
# without further arguments pygraphviz will be used
machine = GraphMachine(model=m, ...)
# when you want to use graphviz explicitly
machine = GraphMachine(model=m, use_pygraphviz=False, ...)
# in cases where auto transitions should be visible
machine = GraphMachine(model=m, show_auto_transitions=True, ...)

# draw the whole graph ...
m.get_graph().draw('my_state_diagram.png', prog='dot')
# ... or just the region of interest
# (previous state, active state and all reachable states)
roi = m.get_graph(show_roi=True).draw('my_state_diagram.png', prog='dot')