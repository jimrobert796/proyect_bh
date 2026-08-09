extends Node2D

var enemyScene = preload("res://scenes/enemy_base.tscn")
var enemyMini = preload("res://scenes/enemy_mini.tscn")

func _ready():
	var e1 = enemyScene.instantiate()
	add_child(e1)
	e1.global_position = Vector2(200, 100)
	
	var e2 = enemyMini.instantiate()
	add_child(e2)
	e2.global_position = Vector2(800, 100)
