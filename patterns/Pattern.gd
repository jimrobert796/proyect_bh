class_name Pattern
extends Node

@export var bulletScene: PackedScene = preload("res://scenes/bullet.tscn")
@export var tiempoFuego = 0.4
@export var duracion = 10.0  # segundos que dura el patrón activo (0 = infinito)

var tempo = 0.0
var tiempoActivo = 0.0
var activo = true
var enemigo: Node2D  # referencia al enemigo dueño (para saber su posición)

signal pattern_terminado  # se emite cuando se acaba la duración

func _ready():
	enemigo = get_parent()

func _process(delta):
	if not activo:
		return

	tempo += delta
	if tempo > tiempoFuego:
		disparar()
		tempo = 0.0

	if duracion > 0:
		tiempoActivo += delta
		if tiempoActivo >= duracion:
			detener()

func detener():
	activo = false
	pattern_terminado.emit()

func reiniciar():
	tempo = 0.0
	tiempoActivo = 0.0
	activo = true

# Cada patrón hijo DEBE sobreescribir esto
func disparar():
	push_warning("disparar() no implementado en este Pattern")

# Método de ayuda reusable por todos los patrones
func crear_bala(direccion: Vector2):
	var bullet = bulletScene.instantiate()
	bullet.direccion = direccion
	get_tree().current_scene.add_child(bullet)
	bullet.global_position = enemigo.global_position
