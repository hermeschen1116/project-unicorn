![logo](unicorn.png)
# Project Unicorn

> NCU machine learning course final project

## Motivation and Goal

- **Motivation**

  At first, we wanted to build a model to predict stock based on the analysis of ptt users' discussion.
  After some research, we found that idea is somewhat difficult for us.
  But fortunately, we discovered an interesting data set on Kaggle which is about the start-ups.
  Also, it's related to our original idea about predicting prospect of a stock/company, so we came up with a new plan based on this data set.

  [Startups Valued at $1 Billion or More](https://www.kaggle.com/datasets/thedevastator/startups-valued-at-1-billion-or-more)
- **Goal**
	- Provide a interactive and fun way to know about start-ups.
	- Give some possible invest targets.
	- Find out the key traits of a company to be successful.
	- Passing the class.

## Related Work / Market Survey

### What is "Unicorn" ?

The term unicorn refers to a privately held startup company with a value of over $1 billion.

### CrunchBase

A web database about start-ups, including various type of data such as founder, finance, and investors, etc.
The original source of the data set we use is from here.

## Users

- **Investors** that are seeking a practical way to know if a start-up will become a unicorn.
- People that are **seeking the chance to enter a start-up**.
- **Startup founders** who want to evaluate the their own or other's company by objective index(s).

## Explanation of Product Features

### Backend: NT-D

> Algorithm to Predict the Future Development of Start-up Companies

### Frontend: La+ Program

> UI to Interact with NT-D

- Features
- [ ] Show the possibility if a start-up will become a unicorn.
- [ ] Show what are in common between unicorns.

## The Solution Architecture

[//]: # (&#40;Describe of product solutions and techniques&#41;)

### Tech Stack

- Python 3.10.8
- [PyTorch](https://github.com/pytorch/pytorch)
- [PyTorch Lightning](https://github.com/pytorch/pytorch)
- [Rust](https://github.com/rust-lang/rust)
- [Tauri](https://github.com/tauri-apps/tauri)

### Architecture
![architecture](architecture.png)

## Reference

[//]: # (https://ithelp.ithome.com.tw/articles/10252383?sc=pt)
