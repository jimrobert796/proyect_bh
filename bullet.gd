extends Area2D

#Hacer poo hacer bullet para enemigo

var speed = 400
var direccion = Vector2(-1,1)
var type = "enemy"

# Called when the node enters the scene tree for the first time.
func _ready():
	if type == "player":
		add_to_group("player_bullets")
	else :
		add_to_group("enemy_bullets")


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	position += direccion * speed * delta
