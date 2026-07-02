# 🎧 Heard

**An AI-assistive wearable For Autistic Children**

Heard is designed as an assistive tool that listens to vocal patterns and displays emotional indicators in a simple visual form, helping create moments of understanding when communication is difficult.

---

# 🌍 Why We Built Heard

The idea for Heard came from a personal experience.

Growing up, I watched my younger brother feel hesitant about interacting with an autistic child in our neighborhood. Much of that hesitation came from misunderstanding and uncertainty rather than anything the child had done.

That experience highlighted a broader problem: many families, and peers struggle to interpret emotional cues when communication happens differently from what they expect.

Heard was created to explore whether AI could provide an additional layer of insight.

---

# 🧠 What is Heard?

Heard is an experimental wearable AI system that analyzes audio and predicts emotional states based on vocal characteristics.

Instead of focusing on words, it looks at patterns within sound, including:

- Pitch
- Energy
- Rhythm
- Changes in vocal patterns over time

The system then converts those signals into an emotion prediction and displays the result through a small wearable interface.

---

# ✨ How It Works

```
Human Voice
      |
      v
  Microphone
      |
      v
 AI Emotion Model
      |
      v
 Arduino Controller
      |
      v
 8x8 LED Display
      |
      v
 Dashboard
```

---

# 🏗️ System Architecture

Heard uses a cross-modal learning approach during training.

### Training Phase

```
           Autism Face Dataset
                    |
                    v
              MobileNetV2
                    |
                    v
            Emotion Features
                    |
                    v

Audio Dataset --> CNN-GRU --> Emotion Prediction
                    |
                    v
            Auxiliary Training
                    |
                    v
      Improved Audio Representation
```

The visual model acts as a teacher during training, helping the audio model learn richer emotional representations.

### Deployment Phase

```
      Audio Input
           |
           v
       CNN-GRU
           |
           v
   Emotion Prediction
           |
           v
     LED Animation
```

Only audio is used during real-world operation.

- No camera
- No facial tracking
- No video recording

---

# 🎧 Audio Features

The system extracts several key audio features.

### MFCC (Mel-Frequency Cepstral Coefficients)

Captures important characteristics of speech, including:

- Voice texture
- Frequency patterns
- Speech dynamics

### Zero Crossing Rate (ZCR)

Measures how often an audio signal changes direction.

Useful for identifying:

- Excited speech
- Harsh sounds
- High-energy vocalizations

### RMS Energy

Measures signal intensity and loudness.

Useful for understanding:

- Emotional intensity
- Energy levels
- Vocal strength

Combined:

```
Audio Features = MFCC + ZCR + RMS
```

---

# 🧬 Deep Learning Model

```
    Audio Features
           |
           v

        1D CNN

           |
           v

   Feature Extraction

           |
           v

          GRU

           |
           v

 Temporal Understanding

           |
           v

 Emotion Classifier
```

### Why CNN + GRU?

The CNN learns meaningful patterns from audio features, while the GRU learns how those patterns evolve over time.

Emotion is rarely expressed in a single instant. It develops across a sequence of sounds, pauses, and changes in tone.

---

# 📊 Results

| Emotion | F1 Score |
|----------|----------|
| 😡 Anger | 91% |
| 😨 Fear | 74% |
| 😊 Happy | 81% |
| 😐 Neutral | 80% |
| 😢 Sad | 77% |

### Overall Performance

**81% Test Accuracy**

Evaluation was performed using speaker-independent testing to better measure generalization to unseen voices.

---

# 🔥 The Biggest Challenge

One of the hardest parts of this project was data.

There are very few publicly available datasets containing emotional audio from autistic children. Most existing emotion datasets rely on:

- Actors
- Controlled recordings
- Simulated emotions

Real emotional expression can vary significantly from person to person, and autistic individuals may communicate emotions differently than conventional datasets suggest.

Because of this, Heard is designed with caution and transparency in mind.

---

# 🤔 Human-Centered AI

Heard does not make absolute claims.

The goal is to provide additional context, not definitive answers.

Human judgment remains essential.

---

# 🖥️ Hardware Prototype

```
Lapel Microphone
        |
        v

Laptop / Edge Device
        |
        v

ONNX AI Model
        |
        v

Arduino UNO
        |
        v

MAX7219 8x8 LED Matrix
```

The LED matrix displays simple emotional animations that can be interpreted quickly and discreetly.

---

# 🧪 Key Lesson

Voice/Mic alone would be somehow difficult to classify autistic children emotion unlike neurotypical people but thats all we got, so its somehow like a research project 
---

# 🚀 Future Development

### Personalized Adaptation

People express emotions differently.

Future versions could learn individual emotional patterns over time, allowing the system to better understand how a specific user expresses happiness, stress, frustration, or excitement.

### Multimodal Understanding

Future versions may incorporate additional signals such as:

- Audio
- Movement

Combining multiple signals could provide a more complete understanding of emotional state.

---

# 🏆 Project Information

**USAII Global AI Hackathon 2026**

Theme:

> AI for Good in Your World

Community Challenge:

> Make Support Obvious

---

# 👥 Team

## AI/ML Empire

### Muhammad Mujahid Haruna

- AI Architecture
- Machine Learning
- Hardware Integration

### Cora Zeng

- Research
- Responsible AI
- Personalization Strategy

---

# ⚠️ Disclaimer

Heard is a research prototype.

It is intended to be:

- An assistive tool
- A communication aid
- A source of additional context

It is not:

- A medical diagnostic system
- A perfect measure of emotional state

---

# ❤️ Heard

**Because understanding should never depend on how easily someone can express themselves.**

Built with curiosity, empathy, and the belief that technology should help people connect more meaningfully with one another.
