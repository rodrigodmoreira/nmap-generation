extends Spatial

export(NodePath) var quad_mesh_path
onready var quad_mesh: MeshInstance = get_node(quad_mesh_path)

var sprite_path: String
var sprite_img: Image
var sprite_tex: ImageTexture

var normal_path: String
var normal_img: Image
var normal_tex: ImageTexture
var normal_strength := 1.0

func _ready() -> void:
	Input.set_mouse_mode(Input.MOUSE_MODE_HIDDEN)
	
	var args = OS.get_cmdline_args()
	if len(args) >= 2:
		sprite_path = args[0]
		normal_path = args[1]
		
		if len(args) == 3 and str(args[2]).is_valid_float():
			normal_strength = float(args[2])
	
	if sprite_path:
		load_sprite()
		load_normal()
		setup_textures()

func load_sprite() -> void:
	sprite_img = Image.new()
	var err := sprite_img.load(sprite_path)
	if err != OK:
		print("Error loading albedo")
		sprite_img.load("res://assets/default_color.png")
	
	sprite_tex = ImageTexture.new()
	sprite_tex.create_from_image(sprite_img, 0)

func load_normal() -> void:
	normal_img = Image.new()
	var err := normal_img.load(normal_path)
	if err != OK:
		print("Error loading normal")
	normal_tex = ImageTexture.new()
	normal_tex.create_from_image(normal_img, 0)

func setup_textures() -> void:
	if is_instance_valid(quad_mesh):
		var tex_size = Vector2(sprite_tex.get_width(), sprite_tex.get_height())
		var screen_size := get_viewport().get_visible_rect().size
		var scale_factor = 1
		if tex_size.x > tex_size.y:
			quad_mesh.scale = .25*Vector3(
				screen_size.x / tex_size.x,
				screen_size.x / tex_size.x,
				1
			)
		else:
			quad_mesh.scale = .25*Vector3(
				screen_size.y / tex_size.y,
				screen_size.y / tex_size.y,
				1
			)
		
		var spt_material: SpatialMaterial = quad_mesh.get_surface_material(0)
		spt_material.albedo_texture = sprite_tex
		spt_material.normal_texture = normal_tex
		spt_material.flags_transparent = true
		spt_material.normal_scale = normal_strength

func _input(event: InputEvent) -> void:
	if event is InputEventKey:
		if event.scancode == KEY_ESCAPE:
			get_tree().quit()


#func _process(delta: float) -> void:
#	if Input.is_action_just_pressed("alternate"):
#		_toggle_normal_sprite()
#
#	if Input.is_action_pressed("zoom_in"):
#		_increase_scale(.1)
#	if Input.is_action_pressed("zoom_out"):
#		_increase_scale(-.1)
#
#func _toggle_normal_sprite() -> void:
#	if is_instance_valid(normal_sprite):
#			print('space',normal_sprite)
#			normal_sprite.visible = not normal_sprite.visible
#
#func _increase_scale(value: float) -> void:
#	if is_instance_valid(sprite):
#				sprite.scale += Vector2(value,value)
