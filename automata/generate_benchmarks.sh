#!/usr/bin/sh

~/bin/bin/randltl p1 --seed=42 -n20 --tree-size=150..250 --output="benchmarks/ltl-1.ltl"

~/bin/bin/randltl p1 p2 --seed=42 -n20 --tree-size=150..250 --output="benchmarks/ltl-2.ltl"

~/bin/bin/randltl p1 p2 p3 --seed=42 -n20 --tree-size=150..250 --output="benchmarks/ltl-3.ltl"

~/bin/bin/randltl p1 p2 p3 p4 --seed=42 -n20 --tree-size=150..250 --output="benchmarks/ltl-4.ltl"

~/bin/bin/randltl p1 p2 p3 p4 p5 --seed=42 -n20 --tree-size=150..250 --output="benchmarks/ltl-5.ltl"
