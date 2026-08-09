class_name EnemigoMini
extends Area2D

@export var vidaMax = 1
@export var tipo = "enemy"
@export var secuenciaPatterns: Array[PackedScene] = [
	preload("res://scenes/test_scene.tscn")
]
@export var loop = true  # si al terminar la lista, vuelve a empezar desde el principio


var vida
var patternActual: Pattern
var indiceActual = 0

func _ready():
	#Variables son modificadas en este constructor
	secuenciaPatterns = [
	preload("res://scenes/test_scene.tscn"),
	preload("res://scenes/spiral_double.tscn")
	]
	vida = 2 # Vida reducida a 2 
	if secuenciaPatterns.size() > 0:
		asignar_pattern(secuenciaPatterns[0])

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
			print("Sigue en pie restante:", vida)
		area.queue_free()
