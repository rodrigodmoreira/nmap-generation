extends Control

export var show_text := false

onready var mousePositionLabel = $MousePositionLabel

var mouse_position: Vector2 = Vector2.ZERO

func _process(delta: float) -> void:
	if show_text:
		mousePositionLabel.text = "M: (?, ?)".format([int(mouse_position.x), int(mouse_position.y)], "?")
	else:
		mousePositionLabel.text = ""

func _physics_process(delta: float) -> void:
	mouse_position = get_global_mouse_position()
