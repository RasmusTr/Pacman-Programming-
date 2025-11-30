# University Assignment: Modular Ghost Game

This project was developed as part of a university assignment. The task was to create a game that follows specific **framework guidelines**, which intentionally constrain the game dynamics. The project was completed within one month.

---

## 🎮 Game Overview

The game is modular and includes the following mechanics:

* **Game Field:**
  The field is generated based on the input `n_1` as follows:

  ```
  Field size = 2^n_1 + 1
  ```

  The field is recursively generated from a pattern and includes **random components**.

* **Enemies:**
  The game includes `n_2` ghosts. They move independently and interact with the player according to the game rules.

* **Power-ups:**

  * Contact with a power-up **slows down the ghosts**.
  * The player becomes **invincible** for a short period.

* **Game Over:**

  * Contact with a ghost **without an active power-up** results in the **player’s death** and **end of the game**.

---

## 🛠 Project Structure

The program is modular and includes the following main components:

```
/src
  /modules        # Contains modules for field generation and enemy logic
  /assets         # Images, icons, and videos
main.py           # Main program that starts the game
README.md         # This file
```

---

## ⚡ Features

* Recursive field generation with random components
* Configurable number of ghosts
* Power-up system affecting player invincibility and ghost speed
* Modular code structure for easy extension

---

## 📸 Screenshots

You can include images here to illustrate the game:

```md
![Different size 1](assets/demo_pic_1.png)
![Different size 2](assets/demo_pic_2.png)
![Game progress 1](assets/demo_pic_3.png)
![Game progress 2](assets/demo_pic_4.png)
```

---

## 📹 Demo Video

Here is a demonstration of the game in action:

<video width="600" controls>
  <source src="assets/demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

---

## ⏱ Development Time

The project was completed over a **one-month period** as part of the assignment requirements.

---

## 🎯 Notes

The game behavior differs slightly from standard implementations due to the **university-assigned constraints**, which shaped the mechanics and design choices.
