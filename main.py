from ursina import *
import random

# 1. אתחול מנוע המשחק ה-3D
app = Ursina()

# הגדרת חלון והעלמת נתוני מערכת מיותרים
window.fps_counter.enabled = False
window.exit_button.enabled = False

# 2. הגדרת סביבה ותאורה (אווירה אפלה ומפחידה)
Sky(color=color.black)
ambient_light = AmbientLight(color=color.dark_gray)
directional_light = DirectionalLight(color=color.gray, direction=(1, -1, 1))

# 3. החדר של השחקן (קוביה כחולה זוהרת במרכז)
player_room = Entity(
    model='cube',
    color=color.cyan,
    scale=(3, 3, 3),
    position=(0, 0, 0),
    texture='white_cube'  # נותן מרקם בסיסי כדי שנראה את התלת-ממד
)
player_label = Text(text="YOUR ROOM (SAFE)", position=(-0.1, 0.1), scale=1.5, color=color.cyan)

# 4. האיום הדיגיטלי - קוביית האויב האדומה שמתחילה מרחוק
enemy_node = Entity(
    model='cube',
    color=color.red,
    scale=(1.5, 1.5, 1.5),
    position=(0, 0, 15),  # מתחילה 15 מטרים קדימה במסדרון הווירטואלי
    texture='white_cube'
)
enemy_label = Text(text="MALWARE DETECTED", position=(0.3, 0.3), scale=1.5, color=color.red)

# 5. הגדרת המצלמה (מבט על תלת-ממדי קולנועי)
camera.position = (0, 10, -20)
camera.rotation_x = 25  # זווית הסתכלות מלמעלה למטה

# משתני משחק
game_over = False


# 6. לולאת המשחק הראשי (רצה בכל פריים מחדש!)
def update():
    global game_over
    if game_over:
        return

    # הנוזקה האדומה מתקדמת לאט לאט לכיוון החדר של השחקן (ציר ה-Z)
    if enemy_node.z > player_room.z + 1.5:
        enemy_node.z -= time.dt * 1.5  # מהירות ההתקדמות

        # סיבוב קל של הקוביה האדומה בשביל אפקט דיגיטלי מגניב
        enemy_node.rotation_y += time.dt * 50
        enemy_node.rotation_x += time.dt * 20
    else:
        # האויב הגיע לחדר - המשחק נגמר!
        game_over = True
        player_room.color = color.red
        enemy_label.text = "SYSTEM COMPROMISED!"
        print("הקוד נפרץ! המשחק נגמר.")


# 7. קלט מהשחקן (מקלדת ועכבר)
def input(key):
    global game_over
    if game_over:
        if key == 'space':  # לחיצה על רווח מאתחלת את המשחק
            enemy_node.position = (0, 0, 15)
            player_room.color = color.cyan
            enemy_label.text = "MALWARE DETECTED"
            game_over = False
        return

    # מנגנון הגנה: אם השחקן לוחץ על 'f' (Firewall), הוא הודף את האויב אחורה!
    if key == 'f':
        enemy_node.z += 3  # דוחף את הנוזקה 3 מטרים אחורה במסדרון
        # אפקט ויזואלי קטן של הדף
        player_room.blink(color.white, duration=0.2)


# הרצת המשחק
app.run()
