def check_collision(bullet, enemy):
    return (bullet.x < enemy.x + enemy.width and
            bullet.x + bullet.width > enemy.x and
            bullet.y < enemy.y + enemy.height and
            bullet.y + bullet.height > enemy.y)

def check_collision_player(player, enemy):
    return (player.x < enemy.x + enemy.width and
            player.x + player.width > enemy.x and
            player.y < enemy.y + enemy.height and
            player.y + player.height > enemy.y)

