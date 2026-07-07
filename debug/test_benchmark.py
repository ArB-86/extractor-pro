
from benchmark.benchmark import Benchmark
from benchmark.report import Report

gold = [

{
"id":1,
"question":"Find x",
"question_type":"numerical",
"difficulty":"easy",
"topic":"algebra"
},

{
"id":2,
"question":"Show that",
"question_type":"proof",
"difficulty":"hard",
"topic":"trigonometry"
}

]

pred = [

{
"id":1,
"question":"Find x",
"question_type":"numerical",
"difficulty":"easy",
"topic":"algebra"
},

{
"id":2,
"question":"Show that",
"question_type":"proof",
"difficulty":"medium",
"topic":"trigonometry"
}

]

results = Benchmark().evaluate(
pred,
gold
)

Report().print(results)
