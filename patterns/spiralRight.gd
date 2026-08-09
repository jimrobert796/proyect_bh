class_name PatternSpiralRight
extends Pattern

@export var incrementoAngulo = 0.2

var angulo = 180

func _ready():
	super._ready()
	tiempoFuego = 0.1
	duracion = 2

func disparar():
	angulo += incrementoAngulo
	crear_bala(Vector2(sin(angulo), cos(angulo)))
