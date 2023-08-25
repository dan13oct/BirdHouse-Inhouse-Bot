import discord
import data_management
import check_user


class SetRolesModal(discord.ui.Modal, title='Set Role Preferences (1-5)'):
    pos1 = discord.ui.TextInput(label='Carry Preference', max_length=1)
    pos2 = discord.ui.TextInput(label='Midlane Preference', max_length=1)
    pos3 = discord.ui.TextInput(label='Offlane Preference', max_length=1)
    pos4 = discord.ui.TextInput(label='Soft Support Preference', max_length=1)
    pos5 = discord.ui.TextInput(label='Hard Support Preference', max_length=1)

    async def on_submit(self, interaction: discord.Interaction):
        pos1 = str(self.pos1)
        pos2 = str(self.pos2)
        pos3 = str(self.pos3)
        pos4 = str(self.pos4)
        pos5 = str(self.pos5)
        try:
            int_pos1 = int(pos1)
            int_pos2 = int(pos2)
            int_pos3 = int(pos3)
            int_pos4 = int(pos4)
            int_pos5 = int(pos5)
            role_list = [int_pos1, int_pos2, int_pos3, int_pos4, int_pos5]
            x = 0
            while x < len(role_list):
                if role_list[x] > 5:
                    role_list[x] = 5
                elif role_list[x] == 0:
                    role_list[x] = 1
                x += 1
            data_management.update_user_data(interaction.user.id, [3, 4, 5, 6, 7], role_list)
            await interaction.response.send_message('Thank you for updating your role preferences', ephemeral=True, delete_after=10)
        except:
            await interaction.response.send_message('Please only use numbers when setting roles',
                                                    ephemeral=True, delete_after=10)


class RegisterUserModal(discord.ui.Modal, title='Player Register'):
    dotabuff_url = discord.ui.TextInput(label='Dotabuff User URL')
    player_mmr = discord.ui.TextInput(label='Player MMR', max_length=5)

    async def on_submit(self, interaction: discord.Interaction):
        server = interaction.user.guild
        role = discord.utils.get(server.roles, name="inhouse")
        disc = interaction.user.id
        steam = str(self.dotabuff_url)
        mmr = str(self.player_mmr)
        try:
            int_mmr = int(mmr)
            if int_mmr > 12000:
                raise Exception('Please enter a valid mmr.')
            if "dotabuff.com/players/" in steam:
                steam = steam.split("players/")
                try:
                    steam = steam[1].split('/')
                    steam = int(steam[0])
                    player = [disc, steam, int_mmr, 5, 5, 5, 5, 5]
                    data_management.add_user_data(player)
                    await interaction.user.add_roles(role)
                    check_user.user_list("Add", interaction.user)
                    await interaction.response.send_message(
                        'You\'ve been registered, please set your roles and wait to be vouched',
                        view=SetRolesModal(), ephemeral=True)
                except:
                    await interaction.response.send_message(
                        'There was an error with the dotabuff url you provided, please try again',
                        ephemeral=True,
                        delete_after=10)
            else:
                await interaction.response.send_message('Please enter your full Dotabuff user url when registering',
                                                        ephemeral=True,
                                                        delete_after=10)
        except ValueError:
            await interaction.response.send_message('Please only enter numbers when providing your MMR',
                                                    ephemeral=True,
                                                    delete_after=10)


class RegisterButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Click to register for inhouse", emoji="📝",
                       style=discord.ButtonStyle.green)
    async def register(self, interaction: discord.Interaction, button: discord.ui.Button):
        server = interaction.user.guild
        role = discord.utils.get(server.roles, name="inhouse")
        if role in interaction.user.roles:
            await interaction.response.send_message(content="You are already registered", ephemeral=True,
                                                    delete_after=10)
        else:
            await interaction.response.send_modal(RegisterUserModal())

    @discord.ui.button(label="View your details", emoji="📋",
                       style=discord.ButtonStyle.blurple)
    async def view_self(self, interaction: discord.Interaction, button: discord.ui.Button):
        server = interaction.guild
        role = discord.utils.get(server.roles, name="inhouse")
        if role in interaction.user.roles:
            user_data = data_management.view_user_data(interaction.user.id)
            await interaction.response.send_message(embed=check_user.user_embed(user_data, interaction.user, server),
                                                    ephemeral=True)
        else:
            await interaction.response.send_message(content="You need to register before you can see your details",
                                                    ephemeral=True)

    @discord.ui.button(label="Update your role preferences", emoji="🖋️",
                       style=discord.ButtonStyle.blurple)
    async def set_roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        server = interaction.guild
        role = discord.utils.get(server.roles, name="inhouse")
        if role in interaction.user.roles:
            await interaction.response.send_modal(SetRolesModal())
        else:
            await interaction.response.send_message(content="Please register before setting roles",
                                                    ephemeral=True)
