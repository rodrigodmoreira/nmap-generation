extends Camera

onready var hud: Control = get_node('../HUD')

var spatial_mouse_position: Vector3 = Vector3.ZERO

func _physics_process(delta: float) -> void:
	if is_instance_valid(hud):
		spatial_mouse_position = project_position(hud.mouse_position, 0)
