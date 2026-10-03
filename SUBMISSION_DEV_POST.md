---
title: "DawaaiDost: helping my grandparents make sense of medicine instructions"
published: false
tags: devchallenge, weekendchallenge, hf26challenge, opensource
canonical_url: false
---

*This is a draft for the [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01).*

## What I Built

I started DawaaiDost (दवाई दोस्त) for my grandparents. The idea came from a familiar family problem: a prescription uses shorthand like `OD`, `BD`, or `AC`, and someone has to help work out what the instructions say and when a medicine is meant to be taken.

DawaaiDost is a small web prototype. You can choose a family profile, paste prescription text or a Hinglish note, and get a structured medicine card with a Hindi instruction that can be read aloud. The page also has controls to add a memory rule and ask a few common questions.

The aim is to make an instruction easier to review together. This prototype is not a medical device, does not verify prescriptions, and should not be used to decide a dose. Always follow the prescriber's instructions and ask a doctor or pharmacist when anything is unclear.

## Demo

Try the live app: [https://dawaaidost.onrender.com](https://dawaaidost.onrender.com)

## Code

Source code: [github.com/nashdev97/dawaaidost](https://github.com/nashdev97/dawaaidost)

## How I Built It

The app is a FastAPI service with a browser interface. The interface sends text to the backend and shows the response as a medicine card.

Here is the important implementation detail: the current deployed parsing path uses deterministic local heuristics. The repository has a Tinker/Qwen integration scaffold, but it does not currently run a fine-tuned open-weight model for inference. The memory feature stores rules in a local JSON file; it is not connected to Backboard. The browser uses its built-in Web Speech API to read instructions; the deployed flow does not use ElevenLabs.

I have not run a reliable model benchmark for this prototype, so I am not claiming an accuracy score. That is a meaningful gap for a medication-related tool, where confident but incorrect instructions could cause harm.

## Why Does Open Innovation Matter?

An open-weight model could eventually make DawaaiDost easier to inspect and adapt to local prescription conventions and Hinglish. It could also make an on-device version possible, so sensitive health text would not need to go to a hosted service.

Those are the reasons I want to explore open models for this project. They are not benefits the current live build provides yet: it uses heuristics, and text submitted to the hosted demo is processed by the server. Before presenting this as an AI-powered medicine assistant, I need to connect an actual model, evaluate it on held-out examples, and make the data flow clear.

## What I Learned

A useful interface can make a prototype feel more capable than its underlying system is. Writing this up made me check what the app actually runs: the model and partner integrations in the code are scaffolding, while the live parsing is heuristic-based. In a health-related use case, being clear about that boundary is part of building responsibly.

## My Agent Session

Optional: add a DevRelay agent-session embed or link here if you have one to share.

## Prize Categories

The app is hosted on Render, so I am entering **Best Use of Render**. I am not entering the Tinker, Backboard, or ElevenLabs categories because those integrations are not active in the deployed user flow.
