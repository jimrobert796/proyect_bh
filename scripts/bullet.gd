extends Area2D

var speed = 400
var direccion = Vector2(-1, 1)
var type = "enemy"

func _ready():
	if type == "player":
		add_to_group("player_bullets")
	else:
		add_to_group("enemy_bullets")

	# Conectamos la señal del notifier hijo
	$VisibleOnScreenNotifier2D.screen_exited.connect(_on_screen_exited)

func _process(delta):
	position += direccion * speed * delta

func _on_screen_exited():
	queue_free()
