extends SpotLight

export var hover_around := true
export var hover_radius := 3.0
export var hover_spd := 0.0015
export var hover_offset := Vector2.ZERO

onready var camera: Camera = get_node("../Camera")
onready var viewport: Viewport = get_viewport()

var mouse_origin := Vector2(785,290)

func _physics_process(delta: float) -> void:
	if hover_around:
		var time := OS.get_ticks_msec()
		translation.x = hover_radius * sin(hover_spd * time - deg2rad(135)) + hover_offset.x
		translation.y = hover_radius * cos(hover_spd * time - deg2rad(135)) + hover_offset.y
	else:
		var mouse_position = camera.spatial_mouse_position
		translation = lerp(translation, Vector3(mouse_position.x, mouse_position.y, translation.z), .15)
	
	_check_set_reset_actions()

func _check_set_reset_actions():
	if Input.is_action_just_pressed("set_light_pos"):
		mouse_origin = get_viewport().get_mouse_position()
	
	if Input.is_action_just_pressed("reset_light_pos"):
		get_viewport().warp_mouse(mouse_origin)
	
	if Input.is_action_just_pressed("toggle_hover"):
		hover_around = not hover_around
