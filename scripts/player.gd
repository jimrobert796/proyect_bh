class_name Player
extends Area2D

@export var velocidad: float = 300.0
@export var velocidad_focus: float = 120.0  # velocidad lenta al mantener Shift (modo preciso)
@export var cooldown_normal: float = 0.08
@export var cooldown_w: float = 0.28  # dispara más lento con W (ui_up) presionado

var bulletScene = preload("res://scenes/bullet.tscn")
var vidas = 3
var limites_pantalla: Rect2
var tempo = 0
var w = false

func _ready():
	print("Estamos listos")
	add_to_group("player")  # <- clave para que los patrones enemigos lo encuentren
	# Ajusta esto al tamaño real de tu ventana/viewport
	limites_pantalla = Rect2(Vector2.ZERO, get_viewport_rect().size)

func _process(delta):
	mover(delta)

# Movimiento general del jugador/personaje
func mover(delta):
	var direccion = Vector2.ZERO

	if Input.is_action_pressed("ui_right"):
		direccion.x += 1
	if Input.is_action_pressed("ui_left"):
		direccion.x -= 1
	if Input.is_action_pressed("ui_down"):
		direccion.y += 1
	if Input.is_action_pressed("ui_up"):
		direccion.y -= 1

	# w solo es true si se presiona arriba SIN izquierda ni derecha a la vez
	if Input.is_action_pressed("ui_up") and not Input.is_action_pressed("ui_left") and not Input.is_action_pressed("ui_right"):
		w = true
	else:
		w = false

	if Input.is_key_pressed(KEY_Z):
		dispararBullet(delta)
	else:
		tempo = cooldown_normal  # listo para disparar de inmediato al volver a presionar

	direccion = direccion.normalized()  # evita que muevas más rápido en diagonal

	var vel_actual = velocidad_focus if Input.is_key_pressed(KEY_SHIFT) else velocidad
	position += direccion * vel_actual * delta


func dispararBullet(delta):
	tempo += delta
	var cooldown_actual = cooldown_w if w else cooldown_normal

	if tempo > cooldown_actual:
		var bullet = bulletScene.instantiate()
		bullet.type = "player"
		bullet.direccion = Vector2(0, -1)
		get_tree().current_scene.add_child(bullet)
		bullet.global_position = global_position
		tempo = 0


func _on_area_entered(area):
	if area.is_in_group(""): #enemy_bullets
		vidas -= 1
		if vidas <= -1:
			print("game over")
			get_tree().paused = true
		else:
			print("vida eliminada, restantes:", vidas)
		area.queue_free()
