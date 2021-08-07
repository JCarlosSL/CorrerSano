
def check_collision(player_x, player_y, player_width, player_height, car_x, car_y, car_width, car_height):
    if (player_x+player_width > car_x) and (
        player_x < car_x+car_width) and (
        player_y < car_y+car_height) and (
        player_y+player_height > car_y):
        return True
    else:
        return False