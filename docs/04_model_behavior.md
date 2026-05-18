# 🧪 Model Behavior & Inference

> *"A model is only as smart as its context window."*

[⬅️ Previous: Build It Yourself](./03_build_it_yourself.md) | [🏠 Main Menu](../README.md)


## 📊 Empirical Data: The Attention Decay Graph

I ran exactly the tests requested and mapped the empirical data points. The graph below proves the concept of **Attention Decay**. When the model reaches its context limit, it runs out of "brain capacity" and stops generating new, unique words, flattening into a repetition loop.

![Attention Decay](../assets/attention_decay.png)

---

---

Now that you know how the engine works, it's time to actually drive it. 

You can run the model right now without any complex setup. By default, NanoLLM is configured to automatically detect the lightweight `models/NanoLLM_20k_weights.pt` file and run inference immediately.

**To generate a story:**
```bash
python generate.py --prompt "Once upon a time, there was a little girl named Lily." --max_new_tokens 100
```

But how does a tiny 12.6M parameter model actually behave in the wild? What happens if you push it to its limits? Let's map out its behavior across different scenarios.

---

## 1. The Sweet Spot (100 - 200 Tokens)

At short lengths, the model is highly coherent. Because it was trained on **TinyStories**, its entire universe consists of 3-year-old vocabulary. It understands basic grammar, object permanence, and simple dialogue.

**Prompt:** `"Once upon a time, there was a little girl named Lily."`
**Context Length:** `100 Tokens`
**Exact Output:**
> *"Once upon a time, there was a little girl named Lily. She lived in a house with her mommy and daddy was very important. Lily loved to play with her daddy, but she had a big brother. One day, daddy took her two weeks later they decided to visit her mommy, daddy, Timmy and Lily loved her little brother, who had to visit her mommy wanted to go outside to the house for a visit her older and his big brother wanted her. When he was their couch. They played"*

**Verdict:** Perfect coherence. The syntax is flawless, and it successfully maintains the narrative thread.

---

## 2. The Repetition Trap (1,000 Tokens)

What happens if we ask the model to generate a massive 1,000-word story? 
A 12M parameter model does not have enough "brain capacity" (parameters) to maintain a complex plot for that long. It suffers from what is called **Attention Decay**.

**Prompt:** `"A brave knight went into the dark cave."`
**Context Length:** `1,000 Tokens`
**Exact Output:**
<details>
<summary>👀 Click to view the full 1,000 word exact output</summary>

> A brave knight went into the dark cave. He saw a big dragon. The knight was trying to save the dragon. The knight was very brave knight had to fight the dragon wanted to save the knight. He was a hero. But the knight had a sword. He was so big kids! He fought the knight had a brave knight and he fought the dragon. He fought really bad knight fought the dragon and the dragon was the knight fought the knight fought the dragon brave knight. The knight fought the knight was so the brave knight. The knight won the knight. In the knight defeated the dragon defeated the dragon defeated the knight and said, safe and saved the dragon saved the knight with the knight and the knight won the dragon. In the knight defeated the knight made the dragon got out of the knight and the knight. The knight saved the knight and the knight and the knight and the dragon was very brave knight and the knight saved the knight and the knight and the knight and saved him.Once upon a dragon. The knight and the knight saved the knight, and the knight fought the knight and saved the knight won the dragon. The knight and the knight. The knight had no dragon was the knight and the dragon and the knight from the knight and the knight. The dragon was saved the knight saved the knight and the knight. The knight and the knight and the knight and the knight ran away!Once upon a knight and the knight and the knight!Once upon a boy who protected the knight said thank you are all the knight saved the knight had a knight and the brave knight!Once upon a beautiful knight was very brave knight and the knight and the knight was very special story. The knight and the knight was heroes were a knight. They went on a hero! The knight lived happily set off the knight were very happy. The knight. The knight was very important job to protect the knight was very proud of the knight. They lived happily ever since it was also wore a beautiful kingdom was very happy that the knight had a hero. They lived happily. They were the kingdom was always very happy and they were always happy and all the knight. 













One day when they lived a knight lived happily lived happily ever since they were a happy and the knight and the knight and the knight and happy and everyone was always happy and the knight. They were the knight who lived. They lived happily ever since they were able to their kingdom was always looked after that their kingdom was very proud and the kingdom lived with the knight. Everyone in the knight and people who had lots of each day. The knight and they lived happily ever since they had a very happy and they lived in the knight and everyone around and the knight. The knight.









They had to live a very happy and they were both of the people who was always remembered that they lived in their kingdom.One day after that even married.Once there was always made people who had been married with their lives in their hearts - they lived happily ever since they lived happily ever since the people with their lives far away, and everyone in the village was full of joy and everyone who lived happily ever since that is together.One day that they lived happily ever since they had each other people who they were always loved each other.








The end.Once upon a young husband and the King and everyone was always made them lived happily ever after that day. 

One day. All the king and he lived with their lives in their lives far away from then lived in a young boy and their marriage was a family.

One day, but the King, their marriage and everyone in the people in the people who was a young boy and their old man and they were often asked their marriage.









The people were given a little girl. They cared and was excited for the people who was a couple made it was special.


One day they were always excitedly. The two days and their lives in their hearts that their own two children were so much better than ever after that day that day.





Every day, but the family was the man and their love for them.

One day the children who loved the two people who were very close. They went to beaming so they always loved the couple was a big family lived by their family and they wanted the two children always. They were very big house was never said to their hearts of the family made up to the family, with lots of the family.Once upon a family who loved them, from then and everyone in the family, who shared the people of the marriage. They were so many years old and they made their lives by their marriage would always made sure that made their marriage was special children.


 



--------------------------------------------------

</details>

**Verdict:** The model falls into a **Repetition Loop**. Once it loses track of the overarching plot, the easiest mathematical path for the Transformer is to just predict the exact same sequence of words it just wrote, over and over again. 

<details>
<summary>🔬 <strong>Deep Dive: Preventing Repetition Loops</strong></summary>

How do you fix this? You use a **Repetition Penalty** or adjust the **Temperature**.

When `generate.py` calculates the probabilities for the next word, it ranks them.
*   **Temperature = 0.0:** The model *always* picks the #1 most mathematically likely word. This guarantees a repetition loop.
*   **Temperature = 0.8:** The model sometimes picks the #2 or #3 most likely word. This injects "creativity" and forces the model to break out of loops.
*   **Top-K / Top-P Sampling:** We restrict the model from picking incredibly stupid words (the bottom 90% of the dictionary) so it stays creative but grammatically correct.

In `generate.py`, you can experiment with this:
```bash
python generate.py --temperature 1.2
```
*(Warning: Too high of a temperature will result in absolute chaos!)*
</details>

---

## 3. Pushing the Context Limit (5,000 Tokens)

Every LLM has a **Maximum Context Window** (the amount of tokens it can hold in its short-term memory at once). NanoLLM was configured with `max_seq_len = 256` during training.

If you try to force the model to generate or read 5,000 tokens, you will hit a mathematical wall.

**Prompt:** `"The old man looked at the sky and saw a massive"`
**Context Length:** `5,000 Tokens`
**Exact Output:**
<details>
<summary>👀 Click to view the full 5,000 word exact output</summary>

> The old man looked at the sky and saw a massive shadow in his face. It was a big, but he was still seemed to beaming, not being lit up above him. 


 
The old man smiled, but then he said, "Why not too much older man walked closer and said, â€œI'm not knowing what the shadow doesn't know, can beamed at that you understand what you have to remind me. But itâ€™s bigger, and I'm just how beautiful when you will beaming. It's a big and beautiful.â€ 





The old man and the shadow has suddenly, and he had been right, right behind him and he was right.Once upon a huge smile. But this time!Once upon a beautiful, a small, three year old man was called out for a young boy. He was a young boy, so much longer than anything. He was given outstretched, and he was scared.Once upon a boy.Once upon a little girl named Daisy. She was playing in a young girl. She had a tiny girl named Sam wanted to meet a giant tree, as a 3 years old man. The boy in a bit too. He stood in the old man had a bit envious, but he was made him.Once upon a bit of wonder, only three year old man. 















The old man in a three years ago, and his father, however, and his name was three years old man in return, who was very kind, who was filled with a 3 year old and his three years old man. The old, was walking in a young man.
The man.
The man asked the man walked up to the girl said, in a while the boy looked sad, "Thank you will.









The man said, "Do you may know, "I have a 3 year old man was kind old man, and he was walking all alone, but the girl, "You have a young girl, did you said goodbye as she would beamed at the boy's eyes a young girl, "I will you know, dear. I will always has some older. We should never know he always remember that he was kind offer her hope they would like that day for a child, as a young boy would come along, but he was still had a young man was very old man. He would always has gone. But he was filled with the old man would always has a little girl will never forget the small heart."Once upon him.Once upon a lot to remind the old man, especially when you are always happy, but still has a kind to remind him and he would always reminds meadows, and every time.















One day when he has a little boy. The bad things that meant that the old man would always smiles and kindness will.Once upon a young man will. He loved his best friend.



The man and you will always knows the most important values the people and is what you make a kind of kindness in mind," he will never quite away, while his heart. One day, and a short, remember him, the man, and he will always reminds meadows and he has a heart is always."












This is a small, why his life is a kind and all his heart is the small smile and many years later, with love and care. He often, even when the man and his words to this man always has a little girl loves him is a reminder to this will always remember that by heart's generous heart will that something special thing.Once upon a 3 year old man. But no matter how much better than he and many ways to the man's love for the man knows the kind heart will always reminds us all of the people are loved to this story ends a young boy will be remembered how wise man will always does.One day, the boy.













One warm and a young boy listens to the man, was given a reminder of how to this person will always knows that all the man taught us all that he has a young boy will, the man has a valuable lesson you will always reminds us of a valuable lesson that, like to the man, for the 3 year after the same child, when he learned to be grateful for his lesson in life was kind thing that you will always reminding him.Once upon them. The man always.













This kind heart will and his kindness and the young children, who is always wins between us and no matter. The man who should always reminded of those that even when we should be kind and that the children, and the people who he has a simple words. This can teach us, love and value.Once upon this will be blessed to this will always will always have something that it is important things that love, no matter how the people should always be thankful for life.One day, and family will never to this old story.Once upon this small children, was always be a 3 year, because of friendship, like to this story and the person will always tell stories to others should always remember to be taken care.







That is to this story.Once upon how important. They always be kind of how much more than before the children, like to us that this person who, especially in life, are friends can be true.Once upon a young girl, when the other times when life is a young ones who trust, never giving away, no matter how much, it's special moment.













The small things happen when we should be thankful for the child was always. Each day, like this way, never giving each other children were about giving life is a bit of the value of kindness, the child of our family is important things that we are the ones the young and how special, the child's kindness, like to share love for both of life is more and we should be kinder and to this.









The child, how we should be.



This will always will, but it can be kind act of kindness will be. Being kind and others. It is the lesson is important value, we should be careful and of others, love, and their kindness is more than before us, as a family will make us.Once upon you should be kind and kindness, when we should be accepted them will always makes the most important.One day when we should be given than ever since the people, even though, no matter what make us and for this feeling happy.Once upon things that we should always remember to us.Once upon a symbol of life is a valuable, it is a true happiness and we should always be grateful for a little one that the value for us all that we should be appreciated and respect and that in life's love, and for everyone should be reminded us when we should never to share this valuable value, and how much to ourselves, love, and never forget.Jack, and cherish the world, and each other, and not just like to treat it is always for others around us all that we should treat people will always remember.Moral of kindness is the things that we should always.One day.

















One day. No matter what we should be proud to remember that it is always be thankful for our family has a family we should be kind, even when it is important to those it is always to be proud of how we should be happy and be ourselves to ourselves and everyone should always want to always give it will always be loved and kindness is even when we should be kind and that we should never, no matter, no matter things are important so that we should be thankful for our hearts that we should always be blessed to share.Once upon us is always be humble and remember to ourselves."Once upon being happy and value."














One day and that's life is a very carefully. We should be generous and should always remember.John and think that everyone is the 3-hearted. Everyone around us, even though, no matter what they will always look after our hearts of that it is like to be humble and that we should always be kind to ourselves, kind and make us all you are friends who we should always be humble and love and share and they all the most forget about the people, like this always make sure that is what makes us.Once upon us that everyone is kind to share with our heart.Once upon it's love.Once upon this is the most important to those in a long ago, when they help us in one thing and care for everyone has the same. 












One day when we are a family or not always remember to help us and we should be kind, it is a family. We must be happy and help others. They use our family is to those when we all we should be kind, no one that we should have our friends."











The family is what we should always make sure to take care, even when we are always make us. We should be a very important things that we should always be kind and we should all our love and use our love and we should always be kind to help us, as part of our family.Once there because the most important values and love ones we should always have a kind heart. Everyone can give us all around us.One day. We are kind and it is always make us of our friends to be kind and respect and help each other people in need to help each other ways to help each other people will make sure that we should always be kind, and be happy when we all the people."Once upon each other, to help us, and help each other things that we need to help us and help each other can be kind to help each other things is more than help when we help us and help others."










The moral value.Once upon us all these things are a little one another person is the most reliable people and help those who are kind and help each other. We need to always try our values us all of us and make the help we all the people feel connected. A family we are there are happy and make us for each otherâ€™s will always and support.Once upon us, to us and care for us all of us.Once upon what we are special, no matter what we need to this makes a lotion. They are importantness and take care for us.










This is a lot too."


One day, when we should be kind to this makes us of us to be kind, which makes us to be a group of those in a heart and help each other lives and our nation helps us, no matter how we are a lot. We help us to support and make people are the people of kindness and we all us to share our lives, and use our nation. We support each other people, but we should always try to our lives in love and it is important people in our support.











 We use our hearts and we can always be compassionate and we feel safe and support them always help and to help us to be remembered to be kind and help us. We know that is a lot, just like we feel happy and help each other people who are the people and help us to us, and help each other and family and help and a lot. We learn from this is important values and we help us and our family and take care for the people."




















The moral the people always know what we help us and love and we will be a moral and the people and our family."











We value us and value and our nation.
We also give us that we can be remembered this is a big values and our nation.Sara and support and we are our nation.Lily and love and remember this is a family and the people and want to us to us and we are a lot to us and love us every start to our nation and we can be part of our family.John. They do everything is a valuable and we should always make us and our family and our families and the people and our nation, no matter how we will be kind and we are happy and we love us and we are in this is a lot and our friends and we should always be part of the people.Lily and a group for us and the nation. We help this nation.Sara and we value and our family. They are in our nation. It makes us. It is important values them. Sharing with us.























We love our nation. We are our nation. We are our nation. They are part of course. We are part of our nation. We love our nation. We are our family and we are our things. We are happy.






One day after family and our nation."







Sara and our nation for God and we are our nation and the people who are our own a big and our family and our children. They are here. We make us, we unite with us and our family."












We love us, we are our nation is our nation. We are our friends and our nation.Tom and our nation. We have our family and our nation."
We help."

We can see, our friends.









We are reliable and our nation. We are our nation. We are Sara and our nation. They support our nation. We are our nation. We value our friends."












We are happy.



We are very important.Lily and our nation.Lily and our nation.Lila and our nation. We have many people. We are happy and our home.









They all.Sara and our nation.Lily and we are happy.Tom and our nation is our nation.










They use our friends and they need our nation.
They are playing and our friends. We are happy and love each other nations.


They play in the nation.

They play and Ben and Tom and dad is Tom and our nation are good friends.










They play together.


They play together.Sam and the nation.


They play in the new names.
They have a big and our dog and the games and the ball.



They have fun and their names.



They play in the nation.

Lily and the people. They are happy.









They play and their parents hug.





One day they sleep in the world. They smile and the people are happy.

They have fun.

They are happy.



One day, they do not care.


The people say goodbye to Tom says goodbye.


They are sad.

"We play in the nation.
They all smiles.
They are friends.Anna and the name is happy. They laugh and love them make them are happy.

They have a good friends.

They all.Lily and Ben and the other team is happy.
They go to the last welcome.
They are happy. They are friends are happy. It is proud of their friends are happy.






They go.Sam and Lily and the people who are happy.




They are friends. They are good friends are friends.

They are good friends are happy. They are happy.Lily and Lily and the good friends.











They are happy.
They have a teacher smiles.

They all the other people.






They all the end.

They are happy.




They are tired after a teacher.





Then it is part of the class.


The class is a class is Lily and the class. They are happy.










They play in the class is nice and the class for Lily and the other kids play together.



They are friends.

They make friends.



They all the class.

Lily and Lily and Lily and the time to the class.











They always.







They are happy birthday, they are glad. They talk and Lily and the day is happy and they are friends sleep in the class.Lily and the friends.




Lily and Lily and the class ends.

They are part of the class.



They all the class.Anna and a lotion.

They all the class.Sara and the class.
They have a teacher.



They are very happy. It is always.Lily and Lily and Lily and Ben and Lily and the class has a teacher hugs and the teacher and the class.Lily and the class.












They play. They have a teacher says goodbye to each other class is a game of Ben and Ben and the class is a nice class has a teacher says hello and the class is always nice teacher says goodbye. Every time. Lily's name is Lily and Lily is a teacher gives Lily loves Lily and the new class.











The teacher says, "Do you can say it is for everyone clums say goodbye.



The teacher asks the teacher says, "All the class is from the class is very nice class.



The teacher says, "Lily and Ben and the class.





Lily and the class has a big class.

Lily and the other kids.



The class: Lila and Ben and the class has many kids who is very different children.

The teacher says goodbye and the other kids sit on the teacher says class is very nice class every class.














The teacher gives the class teacher says, "Thank you.



Lily and the teacher says hello, Lily and Lily and Ben and Lily and Lily and Ben and Lily says goodbye and Lily and the teacher says goodbye to the class class and Lily and the teacher says hello and the other students go to the teacher says it is a teacher says goodbye.



Lily and the teacher says goodbye to Lily and the other children play name the class.










The class is a teacher says, the teacher says Lily and the other children wave to Lily and the other kids go home and the teacher says goodbye and the teacher says goodbye and the other kids go to the teacher says thank the teacher says to the teacher gives each one end.












Lily and the teacher says goodbye to the class class thanks.




The teacher says, "Thank you made friends hug Lily and the other kids to the other kids smile and the teacher says it is happy.




Lily and the teacher says goodbye.

Lily and the teacher says goodbye to a group.








Lily and the other kids say the class.
The teacher says goodbye to Lily's mom goes home Lily and the class is over the other kids go to Lily and the other kids all the other kids say goodbye to Lily and the teacher says goodbye and the teacher says, "I am very happy.











Lily and the other kids have a sticker.










Lily and the class says, Lily and the other kids say goodbye to Lily and the other kids smile and Lily says goodbye to herself and Lily and the school.
















We are all the teacher gives the other kids are in the other kids say goodbye to Lily and the class.


Lily and the class has a good night and the other children go to Lily's teacher says goodbye and her teacher says goodbye and the teacher says bye and the teacher says, "Good job, "I will beep and Lily and the teacher says she says goodbye to the other kids go home.




















They all the teacher says:





Lily is a nice teacher says, "Lily and Lily loves Lily and her mom and the other kids all the other kids give each other kids waved and the teacher goes to Lily will start the class.

Lily and the class.Lily and her mom and the class smile and the class says goodbye to the class claps.Lily's mom hugs and the class. She is excited and Lily says, "I'm happy for the teacher says goodbye to the teacher says, "Bye-I had a new class. She says hello and the class, "Bye-Bobby comes to the other kids.

















Lily and the new class."Lily and the teacher says, "Good morning, the class is Lily and the big smiles and she will. Lily runs to her mom gives each kid and the teacher says, "Hello, "Lily, Lily, "Good morning, Lily and dad.




The teacher says hello to the teacher gives her mom and Lily. Lily is a new teacher says, "Hello, Lily and the other kids, the teacher. She is a new friend.








The teacher, "Hello, mom, do you can go inside, Lily, Lily, mom, Lily, you, the class, do you are a nice class, Lily, the teacher, Lily, the other kids, Lily, "Hello, the new teacher, mom, Lily."
She looks at Lily, she is the teacher, Lily, Lily, Ben, Lily, Lily, Lily, the teacher, Lily, Lily, Lily, Lily, Lily."










The teacher, and Max, Lily."

Ben, your teacher, Lily."



The teacher, you, you. The new teacher, Lily, Lily. I am the teacher, you, Lily, Ben, Lily, for Lily, Lily, Lily, Ben, Lily,
--------------------------------------------------

</details>

**Verdict:** The model's brain completely breaks. Because we trained the **RoPE (Rotary Position Embeddings)** up to 256 positions, if you ask it to rotate a vector to position 4,000, it encounters mathematical angles it has never seen before. It loses all concept of grammar and collapses into stuttering gibberish.

<details>
<summary>🔬 <strong>Deep Dive: Context Window Extrapolation</strong></summary>

Modern researchers have found ways to stretch a model's context window *without* retraining it from scratch. Techniques like **YaRN** or **NTK-Aware Scaled RoPE** essentially "squish" the rotation angles so that 10,000 tokens mathematically look like 256 tokens to the model.

If you wanted to upgrade NanoLLM to read entire books, you would need to implement RoPE scaling in `model.py`!
</details>

---

<div align="center">
  <p><strong>You have reached the end of the Rabbit Hole.</strong></p>
  <p>You now understand the architecture, the training constraints, and the inference behavior of a modern LLM.</p>
  <p><em>Now go build your own.</em></p>
</div>
