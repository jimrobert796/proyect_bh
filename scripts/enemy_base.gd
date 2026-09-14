class_name EnemigoBase
extends Area2D

# Variables para modificar al exportar 
@export var vidaMax = 100 # Vida enemigo
@export var tipo = "enemy" # Tipo proto
@export var secuenciaPatterns: Array[PackedScene] = [
	preload("res://scenes/pattern_boss_phase_1.tscn")
] # Array de patterns a usar
@export var loop = true  # si al terminar la lista, vuelve a empezar desde el principio

# Movimiento simple izquierda-derecha
@export var amplitud_horizontal: float = 150.0  # cuánto se mueve a cada lado desde el origen
@export var velocidad_horizontal: float = 1.0   # qué tan rápido va y viene

var vida
var patternActual: Pattern
var indiceActual = 0
var origen_x: float
var tiempo_movimiento = 0.0

func _ready():
	#Logica a construir (fases, etc lo que sea)
	vida = vidaMax
	origen_x = global_position.x  # guarda su posición horizontal inicial como centro del vaivén
	if secuenciaPatterns.size() > 0:
		asignar_pattern(secuenciaPatterns[0])

func _process(delta):
	tiempo_movimiento += delta
	global_position.x = origen_x + sin(tiempo_movimiento * velocidad_horizontal) * amplitud_horizontal

func asignar_pattern(nuevoPatternScene: PackedScene):
	if patternActual:
		if patternActual.pattern_terminado.is_connected(_on_pattern_terminado):
			patternActual.pattern_terminado.disconnect(_on_pattern_terminado)
		patternActual.queue_free()

	var nuevoPattern = nuevoPatternScene.instantiate()
	add_child(nuevoPattern)
	nuevoPattern.pattern_terminado.connect(_on_pattern_terminado)
	patternActual = nuevoPattern

func _on_pattern_terminado():
	print("El patrón de ", name, " terminó, paso al siguiente")
	indiceActual += 1

	if indiceActual >= secuenciaPatterns.size():
		if loop:
			indiceActual = 0
		else:
			return  # se quedó sin patrones, no dispara más

	asignar_pattern(secuenciaPatterns[indiceActual])

func _on_area_entered(area):
	if area.is_in_group("player_bullets"):
		vida -= 1
		if vida <= 0:
			print("Enemigo derrotado")
			queue_free()
		else:
			print("Sigue en pie")
		area.queue_free()
