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

### TO RUN ON FLY.io

flyctl launch
flyctl secrets set MONGO_URI="mongodb://root:mongodbpassword@mongodb.internal:27017/mydatabase"
flyctl secrets set OPENAI_API_KEY="yourKey"
flyctl deploy

## DONE
* Fine tuned the model with 150 examples. 
* Deployed on render should be up and running by Friday morning
* 126 traning examples of stories that have a 60% trick rate have been stored. 
* New model fine tuned with the above dataset has been deployed. (Cause to switch to new service)
* Prod is live at https://aaai-hackathon.onrender.com/ 

## TODO

* Finish fine tuning the AI models. (Currently on generation 2). Hope to have atleast 4 gneraations of the trained model. 
* Track the user and see their shortcommings and focus on those to trick them further.
* Also add pictures to make it more interactive and fun to read.
* If possible change the voice of the naration to make it sound more real. 

### MONGO CREDS
* cQ7juGaynla0mhbZ
* sdnmvhbdejkvguy

*dbUser
*dbPass


mongodb+srv://dbUser:dbPass@cluster0.cdvas.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0

### Hosted on render
* Its live at https://aaai-hackathon.onrender.com/login/email


### SOME TUINING STUFF
* GEN 0 was not fine tuned
* GEN 1 was tuned with ~60 good examples
* GEN 2 was tuned with data that perfomred well ~150
* GEN 3 and 4 expected to reach around ~500