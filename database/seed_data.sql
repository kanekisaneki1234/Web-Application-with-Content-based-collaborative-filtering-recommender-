-- Sample anime data for testing the recommendation system
-- This file populates the database with initial anime entries

-- Clear existing data
TRUNCATE anime RESTART IDENTITY CASCADE;

-- Insert sample anime data
INSERT INTO anime (title, image_url, genres, description, release_date, rating) VALUES
(
    'Attack on Titan',
    'https://cdn.myanimelist.net/images/anime/10/47347.jpg',
    ARRAY['Action', 'Drama', 'Fantasy', 'Mystery'],
    'Humans are nearly exterminated by giant creatures called Titans. Titans are typically several stories tall, seem to have no intelligence, devour human beings and, worst of all, seem to do it for the pleasure rather than as a food source. A small percentage of humanity survived by walling themselves in a city protected by extremely high walls, even taller than the biggest of titans. Flash forward to the present and the city has not seen a titan in over 100 years. Teenage boy Eren and his foster sister Mikasa witness something horrific as the city walls are destroyed by a super titan that appears out of thin air.',
    '2013-04-07',
    9.0
),
(
    'Death Note',
    'https://cdn.myanimelist.net/images/anime/9/9453.jpg',
    ARRAY['Mystery', 'Psychological', 'Supernatural', 'Thriller'],
    'Light Yagami is an ace student with great prospects—and he is bored out of his mind. But all that changes when he finds the Death Note, a notebook dropped by a rogue Shinigami death god. Any human whose name is written in the notebook dies, and now Light has vowed to use the power of the Death Note to rid the world of evil. But when criminals begin dropping dead, the authorities send the legendary detective L to track down the killer. With L hot on his heels, will Light lose sight of his noble goal...or his life?',
    '2006-10-04',
    8.6
),
(
    'Fullmetal Alchemist: Brotherhood',
    'https://cdn.myanimelist.net/images/anime/1223/96541.jpg',
    ARRAY['Action', 'Adventure', 'Drama', 'Fantasy'],
    'Edward Elric, a young, brilliant alchemist, has lost much in his twelve-year life: when he and his brother Alphonse try to resurrect their dead mother through the forbidden act of human transmutation, Edward loses his brother as well as two of his limbs. With his supreme alchemy skills, Edward binds Alphonse''s soul to a large suit of armor. A year later, Edward, now promoted to the fullmetal alchemist of the state, embarks on a journey with his younger brother to obtain the Philosopher''s Stone.',
    '2009-04-05',
    9.1
),
(
    'Steins;Gate',
    'https://cdn.myanimelist.net/images/anime/5/73199.jpg',
    ARRAY['Sci-Fi', 'Thriller', 'Drama', 'Psychological'],
    'A group of friends have customized their microwave so that it can send text messages to the past. As they perform different experiments, an organization named SERN who has been doing their own research on time travel tracks them down and now the characters have to find a way to avoid being captured by them.',
    '2011-04-06',
    9.0
),
(
    'One Punch Man',
    'https://cdn.myanimelist.net/images/anime/12/76049.jpg',
    ARRAY['Action', 'Comedy', 'Sci-Fi', 'Superhero'],
    'Saitama is a hero who only became a hero for fun. After three years of "special" training, though, he''s become so strong that he''s practically invincible. In fact, he''s too strong—even his mightiest opponents are taken out with a single punch, and it turns out that being devastatingly powerful is actually kind of a bore. With his passion for being a hero lost along with his hair, yet still faced with new enemies every day, how much longer can he keep it going?',
    '2015-10-05',
    8.5
),
(
    'My Hero Academia',
    'https://cdn.myanimelist.net/images/anime/10/78745.jpg',
    ARRAY['Action', 'Comedy', 'Superhero', 'School'],
    'People are not born equal, a realization that 4-year-old Midoriya Izuku faced when bullied by his classmates who had unique special powers. Izuku was one of the rare cases where he was born with absolutely no unique powers. This did not stop Izuku from pursuing his dream, a dream of becoming a great hero like the legendary All-Might. To become the great hero he hopelessly wants to become, he will now join the ranks of one of the highest rated "Hero Academies" in the country: Yueiko. With the help of his idol All-Might, will he be able to claim the ranks and become a true hero?',
    '2016-04-03',
    7.9
),
(
    'Demon Slayer: Kimetsu no Yaiba',
    'https://cdn.myanimelist.net/images/anime/1286/99889.jpg',
    ARRAY['Action', 'Adventure', 'Fantasy', 'Supernatural'],
    'Ever since the death of his father, the burden of supporting the family has fallen upon Tanjirou Kamado''s shoulders. Though living impoverished on a remote mountain, the Kamado family are able to enjoy a relatively peaceful and happy life. One day, Tanjirou decides to go down to the local village to make a little money selling charcoal. On his way back, night falls, forcing Tanjirou to take shelter in the house of a strange man, who warns him of the existence of flesh-eating demons that lurk in the woods at night.',
    '2019-04-06',
    8.7
),
(
    'Code Geass: Lelouch of the Rebellion',
    'https://cdn.myanimelist.net/images/anime/5/50331.jpg',
    ARRAY['Action', 'Drama', 'Mecha', 'Sci-Fi', 'Military'],
    'The Empire of Britannia has invaded Japan using giant robot weapons called Knightmare Frames. Japan is now referred to as Area 11, and its people the 11s. A Britannian who was living in Japan at the time, Lelouch, vowed to his Japanese friend Suzaku that he''d destroy Britannia. Years later, Lelouch is in high school, but regularly skips out of school to go play chess and gamble on himself. One day, he stumbles on terrorists 11s who''ve stolen a military secret and is caught by a member of the Britannian task force sent after them, who is Suzaku.',
    '2006-10-06',
    8.7
),
(
    'Sword Art Online',
    'https://cdn.myanimelist.net/images/anime/11/39717.jpg',
    ARRAY['Action', 'Adventure', 'Fantasy', 'Romance', 'Game'],
    'In the year 2022, virtual reality has progressed by leaps and bounds, and a massive online role-playing game called Sword Art Online (SAO) is launched. With the aid of "NerveGear" technology, players can control their avatars within the game using nothing but their own thoughts. Kazuto Kirigaya, nicknamed "Kirito," is among the lucky few enthusiasts who get their hands on the first shipment of the game. He logs in to find himself, with ten-thousand others, in the scenic and elaborate world of Aincrad, one full of fantastic medieval weapons and gruesome monsters.',
    '2012-07-08',
    7.2
),
(
    'Tokyo Ghoul',
    'https://cdn.myanimelist.net/images/anime/5/64449.jpg',
    ARRAY['Action', 'Horror', 'Drama', 'Supernatural', 'Psychological'],
    'Tokyo has become a cruel and merciless city—a place where vicious creatures called "ghouls" exist alongside humans. The citizens of this once great metropolis live in constant fear of these bloodthirsty savages and their thirst for human flesh. However, the greatest threat these ghouls pose is their dangerous ability to masquerade as humans and blend in with society. Ken Kaneki is a college student who is transformed into a half-ghoul after an encounter with one of these creatures. He must navigate his new life caught between the two worlds of humanity and ghoul society.',
    '2014-07-04',
    7.8
);
