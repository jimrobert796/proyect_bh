class_name PatternAimedShot
extends Pattern

@export var anguloAbanico = 0.25  # separación entre balas, en radianes

var player: Player

func _ready():
	super._ready()
	tiempoFuego = 0.5
	duracion = 8
	player = get_tree().get_first_node_in_group("player")

func disparar():
	if not player:
		return
	var anguloBase = (player.global_position - enemigo.global_position).angle()
	for offset in [-anguloAbanico, 0.0, anguloAbanico]:
		var a = anguloBase + offset
		crear_bala(Vector2(cos(a), sin(a)))
