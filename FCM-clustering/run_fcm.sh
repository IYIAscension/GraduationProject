#!/bin/sh

for iteration in 66304 16389 14706 91254 49890 86054 55284 77324 36147 13506 73920 80157 43981 75358 33399 56134        13388 81617 90957 52113 20428 26482 56340 31018 32067 13067 8339 49008 125894 68282
do
  echo "RUN SCRIPT: $iteration";
  python C:/Users/rasjaad/Desktop/thesis-mutation-testing/FCM-clustering/main.py "C:/Users/rasjaad/Desktop/experiment_results" "$iteration"
done;
