import tkinter as tk
from tkinter import messagebox
from time import sleep
import threading


# TO DO LIST 18/1/19:
# When player loads in their save adjust increment amount accordingly.
# Add comments to all methods in CookieClickerApp class.
# Format Code.
# Code Cleanup

class CookieClickerApp:
    def __init__(self):
        self.xp = 0  # Keeps track of the player's XP
        self.efficiency_tier = 0  # Keeps track of the amount of times player has upgraded their efficiency skill
        self.church_tier = 0  # Keeps track of the amount of times player has upgraded the church assistance skill
        self.bakery_tier = 0  # Keeps track of the amount of times player has upgraded the bakery assistance skill.
        self.total_amount_of_cookies = 0  # Shows how many cookies the player has earned
        self.level_counter = 0  # Player level
        self.increment_amount = 5  # How much XP or cookies to give to the player every click. Upgrading the efficiency tier makes this higher.
        self.eligible_for_upgrade = False  # This tells the computer if the player can upgrade one of their skills.
        self.main_window = tk.Tk()
        self.main_window.title('Cookie Clicker')
        self.main_window.resizable(height=False, width=False)
        self.image_button = tk.Button(command=self.increase_xp)
        self.image_button.grid(row=0)
        msg_to_display = 'Current level:{}'.format(self.level_counter)
        self.level_display = tk.Label(text=msg_to_display)
        self.level_display.grid(row=1)
        xp_display_msg = 'XP:{}'.format(self.xp)
        self.xp_display = tk.Label(text=xp_display_msg)
        self.xp_display.grid(row=2)
        self.upgrades_button = tk.Button(text='Upgrades Menu', command=self.upgrades_menu)
        self.upgrades_button.grid(row=4)
        self.save_button = tk.Button(text='Save Progress', command=self.save_progress_prompt)
        self.save_button.grid(row=5)
        self.load_progress_button = tk.Button(text='Load Progress', command=self.load_progress_prompt)
        self.load_progress_button.grid(row=6)
        amount_of_cookies_display = 'Total Cookies: {}'.format(self.total_amount_of_cookies)
        self.total_amount_display = tk.Label(text=amount_of_cookies_display)
        self.total_amount_display.grid(row=3)
        image_to_display = self.get_image()
        self.image_button.config(image=image_to_display)
        self.main_window.mainloop()

    def load_progress_prompt(self):  # Draws the window that the player can use to load their save game.
        load_progress_window = tk.Toplevel()
        load_progress_window.resizable(width=False, height=False)
        load_progress_window.title('Load Progress')
        save_name_label = tk.Label(load_progress_window, text='Save name:')
        save_name_label.grid(row=0)
        save_name_entry = tk.Entry(load_progress_window)
        save_name_entry.grid(row=0, column=1)
        load_progress_button = tk.Button(load_progress_window, text='Load Progress',
                                         command=lambda:self.load_progress(save_name_entry.get()))
        load_progress_button.grid(row=1, column=1)

    def load_progress(self, save_name):  # Loads progress for the player. Is tied to load_progress_button from window.
        print('Loading from save game {}'.format(save_name))
        try:
            if '.' in save_name:
                pass
            else:
                save_name = '.' + save_name
            with open(save_name, 'r') as save_game_document:
                content = save_game_document.readlines()
            formatted_content = []
            for item in content:
                item = item.strip('\n')
                formatted_content.append(item)
            stat_count = 0  # Keeps track of what line the program is on when reading save file.
            for stats in formatted_content:
                stat_count += 1
                stats_split = stats.split(':')  # Splits up the text so the stats can be easily accessible.
                stat = stats_split[1]
                if stat_count == 1:  # On the first line the player's level is stored.
                    self.level_counter = int(stat)
                elif stat_count == 2: # On the second line the player's xp is stored.
                    self.xp = int(stat)
                elif stat_count == 3:  # On the third line the player's cookies is stored.
                    self.total_amount_of_cookies = int(stat)
                elif stat_count == 4:  # On the fourth line the player's efficiency_tier value is stored!
                    self.efficiency_tier = int(stat)
                elif stat_count == 5:  # On the fifth line the player's church tier is stored.
                    self.church_tier = int(stat)
                elif stat_count == 6:  # On the last line the player's bakery tier is stored!
                    self.bakery_tier = int(stat)

            for x in range(0, self.efficiency_tier):  # Increments the player's efficiency by 5 for every 'x'
                self.increment_amount += 5

            bakery_tier_count = 0  # Keeps track of what tier the player is on.
            # If the tier is below 5 then the player only gets 5 extra cookies per 10 seconds.
            for x in range(0, self.bakery_tier):
                bakery_tier_count += 1
                if bakery_tier_count < 5:
                    self.baker_worker_thread(5)
                else:
                    self.baker_worker_thread(10)

            # The following code are just in case of an error. REMOVE AFTER DONE!
            print('LVL: {}'.format(self.level_counter))
            print('XP: {}'.format(self.xp))
            print('Total amt of cookies: {}'.format(self.total_amount_of_cookies))
            print('Eff Tier: {}'.format(self.efficiency_tier))
            print('Church Tier: {}'.format(self.church_tier))
            print('Bakery Tier: {}'.format(self.bakery_tier))
            xp_msg = 'XP:{}'.format(self.xp)  # The message for self.xp_display to display
            level_msg = 'Current level:{}'.format(self.level_counter)  # The message for self.level_display to show.
            total_cookies_msg = 'Total cookies: {}'.format(self.total_amount_of_cookies)
            self.xp_display.config(text=xp_msg)
            self.level_display.config(text=level_msg)
            self.total_amount_display.config(text=total_cookies_msg)
            messagebox.showinfo('Save loaded!', 'Your save has been loaded!')
        except FileNotFoundError:
            messagebox.showerror('Save not found!', 'That save was not found!')

    def save_progress_prompt(self): # Provides the window for saving your current game.
        save_progress_window = tk.Toplevel()
        save_progress_window.title('Save Progress')
        save_progress_window.resizable(width=False, height=False)
        save_name_label = tk.Label(save_progress_window, text='Save name:')
        save_name_label.grid(row=0)
        save_name_entry = tk.Entry(save_progress_window)
        save_name_entry.grid(row=0, column=1)
        save_button = tk.Button(save_progress_window, text='Save',
                                command=lambda: self.save_progress(save_name_entry.get(), save_progress_window))
        save_button.grid(row=1, column=1)

    def save_progress(self, save_name, window): # Saves the player's game progress into a file name of their choosing.
        if '.' in save_name:
            pass
        else:
            save_name = '.' + save_name
        with open(save_name, 'w') as save_document:
            save_document.write('Level:{}'.format(self.level_counter))
            save_document.write('\n')
            save_document.write('XP:{}'.format(self.xp))
            save_document.write('\n')
            save_document.write('Total Cookies:{}'.format(self.total_amount_of_cookies))
            save_document.write('\n')
            save_document.write('Efficiency Tier:{}'.format(self.efficiency_tier))
            save_document.write('\n')
            save_document.write('Church Tier:{}'.format(self.church_tier))
            save_document.write('\n')
            save_document.write('Bakery Tier:{}'.format(self.bakery_tier))
        messagebox.showinfo('Saved!', 'Your progress has been saved!')
        window.destroy()

    def upgrades_menu(self):  # Provides the window for the player's upgrade menu.
        baker_upgrade1_description = 'Bakers Assistance - 5 cookies every 5 seconds with a cool down of 10 seconds - ' \
                                     'need at least 300 cookies - unlocks at level 2'
        efficiency_upgrade1_description = 'Efficiency Upgrade - 5 more cookies per click - need at least 100 cookies' \
                                          '- unlocks at level 1'
        church_assistance_upgrade1_description = 'Assistance from the local church group, 10 cookies per 5 seconds' \
                                                 ' need at least 500 cookies - unlocks at level 3 '
        upgrades_window = tk.Toplevel()
        upgrades_window.title('Upgrades - Cookie Clicker')
        upgrades_window.resizable(width=False, height=False)
        efficiency_upgrade = tk.Button(upgrades_window, text=efficiency_upgrade1_description,
                                       command=lambda: self.apply_efficiency_upgrades(5, self.level_counter, None, 100))
        efficiency_upgrade.grid(row=0)
        bakery_assistance = tk.Button(upgrades_window, text=baker_upgrade1_description,
                                      command=lambda: self.apply_bakers_upgrade(5, self.level_counter, 2, 300))
        bakery_assistance.grid(row=1)
        church_assistance_button = tk.Button(upgrades_window, text=church_assistance_upgrade1_description,
                                             command=lambda: self.apply_church_assistance(10, self.level_counter,
                                                                                          3, 500))
        church_assistance_button.grid(row=2)

    def church_assistance(self, increment_amount): # This function should be run in a thread to assist the player!
        while True:
            self.xp += increment_amount
            new_xp_count = 'XP:{}'.format(self.xp)
            self.total_amount_of_cookies += increment_amount
            new_total = 'Total cookies:{}'.format(self.total_amount_of_cookies)
            self.xp_display.config(text=new_xp_count)
            self.total_amount_display.config(text=new_total)
            sleep(5)

    def church_assistance_start_thread(self, increment_amount): # Worker thread for self.church_assistance()
        threading.Thread(target=self.church_assistance, args=(increment_amount,)).start()

    def apply_church_assistance(self, increment_amount, player_level, level_requirement, amount_of_cookies_needed):
        # This function checks if the player has met all the requirements to upgrade.
        if self.eligible_for_upgrade is True:
            if player_level == level_requirement and self.total_amount_of_cookies >= amount_of_cookies_needed:
                self.total_amount_of_cookies -= amount_of_cookies_needed
                new_cookie_count = 'Total cookies:{}'.format(self.total_amount_of_cookies)
                self.total_amount_display.config(text=new_cookie_count)
                self.church_assistance_start_thread(increment_amount)
                messagebox.showinfo('Church upgraded!', 'You have upgraded your church tier!')
                self.church_tier += 1
                self.eligible_for_upgrade = False
            else:
                messagebox.showinfo('Not allowed!', 'Please make sure you have enough cookies and are a high enough level for this upgrade!')
        else:
            messagebox.showinfo('Not allowed!', 'You are not eligible for an upgrade! Level up first!')

    def baker_assistance(self, increment_amount):  # This function needs to be run in a thread as well!
        # This function runs in a continuous loop and gives the player 5 cookies every 10 seconds.
        while True:
            self.xp += increment_amount
            self.total_amount_of_cookies += increment_amount
            # self.total_amount_of_cookies -= 5
            new_xp_count = 'XP:{}'.format(self.xp)
            new_total_count = 'Total cookies:{}'.format(self.total_amount_of_cookies)
            self.xp_display.config(text=new_xp_count)
            self.total_amount_display.config(text=new_total_count)
            sleep(10)
            # sleep(10)

    def baker_worker_thread(self, cookies_boost_amount):
        # Function that is responsible for putting the baker_assistance() function into a thread
        print('Increment count: {}'.format(cookies_boost_amount))
        threading.Thread(target=self.baker_assistance, args=(cookies_boost_amount,)).start()

    def apply_bakers_upgrade(self, bakers_increment_amount, player_level, level_requirement, amount_of_cookies_needed):
        # Checks if the player meets the requirement for purchasing this certain upgrade
        if self.eligible_for_upgrade is True:
            if player_level == level_requirement and self.total_amount_of_cookies >= amount_of_cookies_needed:
                self.total_amount_of_cookies -= amount_of_cookies_needed
                updated_cookie_count = 'Total Cookies:{}'.format(self.total_amount_of_cookies)
                self.total_amount_display.config(text=updated_cookie_count)
                self.baker_worker_thread(bakers_increment_amount)
                self.bakery_tier += 1
                messagebox.showinfo('Bakers upgrade complete!', 'You now get {} more cookies every 10 seconds!'.format(bakers_increment_amount))
            else:
                messagebox.showinfo('Error', 'You need to be a level {} for this upgrade!'.format(level_requirement))
        else:
            messagebox.showinfo('Error', 'You are not eligible for an upgrade!')

    def apply_efficiency_upgrades(self, to_increase, player_level, level_requirement, amount_of_cookies_needed):
        # Checks if the player meets the requirement for purchasing an efficiency upgrade.
        print(self.eligible_for_upgrade)
        if self.eligible_for_upgrade is True:
            if level_requirement is None:
                if self.total_amount_of_cookies >= amount_of_cookies_needed:
                    self.total_amount_of_cookies  -= amount_of_cookies_needed
                    updated_cookie_count = 'Total Cookies:{}'.format(self.total_amount_of_cookies)
                    self.total_amount_display.config(text=updated_cookie_count)
                    self.increment_amount += to_increase
                    print(self.increment_amount)
                    messagebox.showinfo('Successful!', 'You now get {} more cookies per click!'.format(to_increase))
                    self.efficiency_tier += 1
                    self.eligible_for_upgrade = False
            else:
                if player_level == level_requirement and self.total_amount_of_cookies >= amount_of_cookies_needed:
                    self.increment_amount += to_increase
                    print(self.increment_amount)
                    messagebox.showinfo('Successful!', 'You now get {} more cookies per click!'.format(to_increase))
                    self.efficiency_tier += 1
                    self.eligible_for_upgrade = False
                else:
                    messagebox.showinfo('Not a high enough level!', 'You need to be level {} to use this!'.format(level_requirement))
        else:
            messagebox.showinfo('Nice Try!', 'You cannot buy another upgrade yet! You have to level up first!')

    def upgrade_player(self, level):
        # This code is run when check_xp_amount detects the player has got enough xp to advance to the next level.
        level_msg = 'You have reached level {}!'.format(level)
        self.eligible_for_upgrade = True
        messagebox.showinfo('Leveled up!', level_msg)
        self.xp = 0
        self.level_counter = level
        xp_msg = 'XP:{}'.format(self.xp)
        level_msg = 'Current level:{}'.format(self.level_counter)
        self.xp_display.config(text=xp_msg)
        self.level_display.config(text=level_msg)

    def check_xp_amount(self):
        # This checks if the player has a enough xp to upgrade, if so then self.upgrade_player() is called.
        if self.level_counter == 0:
            if self.xp == 100:
                self.upgrade_player(1)
        elif self.level_counter == 1 and self.xp >= 300:
            self.upgrade_player(2)
        elif self.level_counter == 2 and self.xp >= 500:
            self.upgrade_player(3)

    def increase_xp(self):
        # This is run every time the cookie is pressed.
        # The player's xp and total amount of cookies increased by the value of self.increment_amount.
        # print(self.xp)
        self.xp += self.increment_amount
        self.total_amount_of_cookies += self.increment_amount
        new_total = 'Total Cookies:{}'.format(self.total_amount_of_cookies)
        new_xp_amount = 'XP:{}'.format(self.xp)
        self.total_amount_display.config(text=new_total)
        self.xp_display.config(text=new_xp_amount)
        self.check_xp_amount()

    @staticmethod
    def get_image():  # This gets the image 'cookie.png' from the directory this script is being run in!
        image = tk.PhotoImage(file='cookie.png')
        return image


app = CookieClickerApp()
