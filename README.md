# Increasing critical thinking in humans in usin AI


## Team Members
* Ashwin R Bharadwaj
* Ankit 


## Types of misinformation 
* Types of Misinformation (Ranked from Easy to Hard for Humans to Detect)
* Basic factual inaccuracies – Wrong names, dates, or figures.
* Contradiction – The fake summary contradicts the original.
* Missing Context / Inaccurate History – Key details are omitted or history is rewritten.
* Irrelevant Detail – Unrelated information is added to mislead.
* Anecdotal Evidence – A single case is generalized as if it applies broadly.
* Underlying Argument Falls Apart (Bad Math/Basic Science Mistakes) – Incorrect data or logical flaws.
* Causation Confused with Correlation – Suggesting that one event caused another when they are just correlated.
* Underlying Scientific Concept is Impossible – Violates known scientific principles.
* Probability of Scenario is Too Improbable – Something that is theoretically possible but so unlikely that it’s misleading.

### Affiliated with Northeastern University 


## Architecture

### TOO RUN LOCALLY
pip install requirments.txt
python app.py -d
docker run -d --name mongo_news -p 27017:27017 -v mongo_data:/data/db mongo


## DONE
* Fine tuned the model with 150 examples. 
* Deployed on fly.io should be up and running by Friday morning
* Need to collect more data and fine tune over the weekend.

## TODO

* Finish fine tuning the AI models.
* Track the user and see their shortcommings and focus on those to trick them further.
* Also add pictures to make it more interactive and fun to read.
* If possible change the voice of the naration to make it sound more real. 