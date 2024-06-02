# Proactive-Sales-Agent
[中文](README_ZH.md)

An experiment to introduce **time concept** to LLM sales agent so it feels the time flying when talking to customers, which aims to enable its natural **proactive talking**.

## Use
Write your API key into [api-config.json](models/api-config.json). Then
```
python app.py
```
## How it works
Remind the LLM periodically how long it has been since last time customers spoke, then the LLM will decide whether to speak or keep silent.
## Results
It needs to be improved. Now it can only do simple things like reminding you how long it's been waiting for you if you ask him to remind you in advance.
## Future
- Besides prompt engineering, finetune it to improve its time concept.
