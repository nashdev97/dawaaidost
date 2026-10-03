---
title: "DawaaiDost: making confusing medicine instructions easier for my grandparents"
published: false
tags: devchallenge, weekendchallenge, hf26challenge, opensource
canonical_url: false
---

*This is a draft for the [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01).*

## What I Built

My grandparents sometimes need help making sense of medicine instructions: what a prescription abbreviation means, when a dose is meant to be taken, and how to read small print on a medicine strip.

I started **DawaaiDost (दवाई दोस्त)** as a family-focused prototype. It accepts pasted prescription text or a Hinglish note, selects a family profile, and displays a structured medicine card with a Hindi instruction that can be read aloud. There are also simple memory controls for adding a rule and asking common questions.

The goal is to make medication instructions easier for an older family member to review with someone they trust. DawaaiDost is a prototype, not a medical device or a substitute for a clinician or pharmacist. The output must be checked against the prescription and confirmed with a healthcare professional.

## Demo

Try the live app: [https://dawaaidost.onrender.com](https://dawaaidost.onrender.com)

## Code

Source: [github.com/nashdev97/dawaaidost](https://github.com/nashdev97/dawaaidost)

## How I Built It

The app uses FastAPI for its endpoints and serves a small browser UI. The UI sends prescription text to the backend and renders the returned fields as a medicine card.

The repository includes a Tinker integration scaffold for Qwen, a local parsing fallback, a JSON-backed memory module, and an ElevenLabs client. The current parsing path in the checked-in app uses deterministic local heuristics; it does not call a fine-tuned model for inference. The memory module currently saves JSON locally rather than calling Backboard, and the browser speaks the Hindi text with its built-in Web Speech API. Those distinctions matter: the live demo should be understood as an early prototype, not as a deployed fine-tuned medical model or a production memory service.

## Why Does Open Innovation Matter?

An open-weight model could make this kind of tool easier to inspect, adapt for local language and prescription conventions, and run closer to a family's own device. The code is open so others can examine the approach and help improve it.

The current build does not yet deliver those model and privacy benefits: its parsing is heuristic-based, and the hosted app processes requests on a server. My next step is to connect and evaluate an actual open-weight model, then make the data flow and privacy choices clear before anyone relies on it.

## My Agent Session

Optional: add a DevRelay agent-session embed or link here if one is available.

## Prize Categories

The app is deployed on Render, so I am entering **Best Use of Render**. I am not claiming the Tinker, Backboard, or ElevenLabs categories for the current build: their production integrations are not active in the deployed parsing and narration flow.
