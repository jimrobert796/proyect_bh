class_name PatternSpiralLeft
extends Pattern

@export var incrementoAngulo = 0.2

var angulo = 0.0

func _ready():
	super._ready()      # ejecuta el _ready() de Pattern (asigna `enemigo`)
	tiempoFuego = 0.1    # ahora sí podés reasignar el valor heredado
	duracion = 2

func disparar():
	angulo += incrementoAngulo
	crear_bala(Vector2(cos(angulo), sin(angulo)))
