# TruthDetect AI: Exposing Misinformation with AI

## Summary

TruthDetect AI is an innovative web application powered by a fine-tuned Large Language Model (LLM) designed to educate users on misinformation by generating both real and fake summaries of products, news, and historical events. The system explains the logical, statistical, and reasoning techniques it uses to craft fake summaries, helping users develop critical thinking skills to identify misinformation.

## Key Features

* Interactive Web App: Users can log in or access the platform as a guest to engage with real and fake summaries.

* Fact or Fiction Challenge: Users analyze a single report and determine if it is true or false. If fooled, the AI provides an explanation.

* Dual-Summary Comparison: Users evaluate two summaries—one real, one fake—and identify the fabricated one. If they mistake the real for fake, the AI explains how misinformation was crafted.

* Adaptive AI Voice Engine: The system uses text-to-speech with evolving accents and speech patterns, optimized through Upper Confidence Bound (UCB) reinforcement learning to increase deception rates.

* Personalized Learning: The AI tracks a user’s weaknesses in specific topics and tailors challenges to improve their understanding in those areas.

## Live Demo

Try it now: TruthDetect AI Web App🔹 Current Version: v0.0.4

## Technical Overview

### LLM Model

* The core model is a fine-tuned GPT-3.5.

* Training data includes 200 hand-curated examples from GPT-4 and DeepSeek, validated by human participants.

* Data selection involved filtering 46 high-quality summaries (real & fake) that successfully deceived humans at a rate of 56%.

* The model was fine-tuned to recognize topic categories and deception techniques.

* A reinforcement learning loop was implemented:

    * Fake summaries that successfully tricked users were continuously used to retrain the model, improving deception capabilities.

    * Over 30 participants tested the model, generating 1000+ summaries, with 712 successful deceptions.

    * The AI constantly learns and adapts, improving over time in misinformation generation and detection.

## Use Cases

Why this matters: Misinformation is a growing concern in today’s digital landscape. TruthDetect AI helps:

* Children & Students – Learn to spot fake news and propaganda through an engaging and interactive experience.

* Investors – Avoid financial traps by identifying fake product reviews and misleading corporate narratives.

* General Public – Recognize deceptive crowdfunding campaigns and fraudulent marketing techniques.

* Political Awareness – Understand how political misinformation is created and spread, and how to critically analyze news sources.

## Future Improvements

* Enhanced Voice Manipulation: Further refining voice adaptation to maximize deception and learning.

* Expanded Dataset: Continuous user testing to collect new data for improving model accuracy.

* Gamification Elements: Introducing a scoring system to engage users in improving their misinformation detection skills.

* Multi-Language Support: Expanding accessibility to different languages and cultural misinformation patterns.

Created for AAAI Hackathon 2025