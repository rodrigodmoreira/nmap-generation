extends MeshInstance

func _process(delta: float) -> void:
	if Input.is_action_pressed("zoom_in"):
		_increase_scale(.1)
	if Input.is_action_pressed("zoom_out"):
		_increase_scale(-.1)
	
#	if Input.is_action_just_pressed("alternate"):
#		_toggle_normal_sprite()

#func _toggle_normal_sprite() -> void:
#	if is_instance_valid(normal_sprite):
#			print('space',normal_sprite)
#			normal_sprite.visible = not normal_sprite.visible

func _increase_scale(value: float) -> void:
	scale += Vector3(value, value, 0)
