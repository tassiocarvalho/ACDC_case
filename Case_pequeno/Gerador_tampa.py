import FreeCAD as App
import Part
import FreeCADGui as Gui

doc = App.newDocument("PlacasDuplas")

# Dimensões da placa menor (interna)
comp_base_menor = 65
larg_base_menor = 37
alt_base = 3  # Altura de 3mm

# Dimensões da placa maior (externa)
comp_base_maior = 71
larg_base_maior = 53

# Raio para arredondar os cantos
raio_canto = 3

# Calcular deslocamento para centralizar a placa menor dentro da maior
dx = (comp_base_maior - comp_base_menor) / 2
dy = (larg_base_maior - larg_base_menor) / 2

# ===== CRIAR PLACA MENOR (92x57) =====
# Começar com um retângulo menor (sem os cantos)
base_meio_menor = Part.makeBox(comp_base_menor - 2*raio_canto, larg_base_menor, alt_base)
base_meio_menor.translate(App.Vector(raio_canto + dx, dy, 0))

# Criar retângulos laterais
lateral_esq_menor = Part.makeBox(raio_canto, larg_base_menor - 2*raio_canto, alt_base)
lateral_esq_menor.translate(App.Vector(dx, raio_canto + dy, 0))

lateral_dir_menor = Part.makeBox(raio_canto, larg_base_menor - 2*raio_canto, alt_base)
lateral_dir_menor.translate(App.Vector(comp_base_menor - raio_canto + dx, raio_canto + dy, 0))

# Criar cilindros nos cantos da placa menor
canto_inf_esq_menor = Part.makeCylinder(raio_canto, alt_base, App.Vector(raio_canto + dx, raio_canto + dy, 0))
canto_inf_dir_menor = Part.makeCylinder(raio_canto, alt_base, App.Vector(comp_base_menor - raio_canto + dx, raio_canto + dy, 0))
canto_sup_esq_menor = Part.makeCylinder(raio_canto, alt_base, App.Vector(raio_canto + dx, larg_base_menor - raio_canto + dy, 0))
canto_sup_dir_menor = Part.makeCylinder(raio_canto, alt_base, App.Vector(comp_base_menor - raio_canto + dx, larg_base_menor - raio_canto + dy, 0))

# Unir todas as partes da placa menor
placa_menor = base_meio_menor.fuse(lateral_esq_menor).fuse(lateral_dir_menor).fuse(canto_inf_esq_menor).fuse(canto_inf_dir_menor).fuse(canto_sup_esq_menor).fuse(canto_sup_dir_menor)

# ===== CRIAR PLACA MAIOR (95x60) =====
# Começar com um retângulo menor (sem os cantos)
base_meio_maior = Part.makeBox(comp_base_maior - 2*raio_canto, larg_base_maior, alt_base)
base_meio_maior.translate(App.Vector(raio_canto, 0, 0))

# Criar retângulos laterais
lateral_esq_maior = Part.makeBox(raio_canto, larg_base_maior - 2*raio_canto, alt_base)
lateral_esq_maior.translate(App.Vector(0, raio_canto, 0))

lateral_dir_maior = Part.makeBox(raio_canto, larg_base_maior - 2*raio_canto, alt_base)
lateral_dir_maior.translate(App.Vector(comp_base_maior - raio_canto, raio_canto, 0))

# Criar cilindros nos cantos da placa maior
canto_inf_esq_maior = Part.makeCylinder(raio_canto, alt_base, App.Vector(raio_canto, raio_canto, 0))
canto_inf_dir_maior = Part.makeCylinder(raio_canto, alt_base, App.Vector(comp_base_maior - raio_canto, raio_canto, 0))
canto_sup_esq_maior = Part.makeCylinder(raio_canto, alt_base, App.Vector(raio_canto, larg_base_maior - raio_canto, 0))
canto_sup_dir_maior = Part.makeCylinder(raio_canto, alt_base, App.Vector(comp_base_maior - raio_canto, larg_base_maior - raio_canto, 0))

# Unir todas as partes da placa maior
placa_maior = base_meio_maior.fuse(lateral_esq_maior).fuse(lateral_dir_maior).fuse(canto_inf_esq_maior).fuse(canto_inf_dir_maior).fuse(canto_sup_esq_maior).fuse(canto_sup_dir_maior)

# ===== FUROS NA PLACA MENOR =====
# Parâmetros dos furos
raio_furo = 1.9
dist_margem_largura = 5  # 0.3 cm = 3 mm
dist_margem_comprimento = 3  # 0.5 cm = 5 mm
altura_furo = alt_base + 1  # cilindro um pouco maior para garantir corte completo

# Centros dos furos próximos às pontas (considerando posição da placa menor)
centros_furos = [
    (dist_margem_comprimento + dx, dist_margem_largura + dy),  # inferior esquerdo
    (comp_base_menor - dist_margem_comprimento + dx, dist_margem_largura + dy),  # inferior direito
    (dist_margem_comprimento + dx, larg_base_menor - dist_margem_largura + dy),  # superior esquerdo
    (comp_base_menor - dist_margem_comprimento + dx, larg_base_menor - dist_margem_largura + dy)  # superior direito
]

# Criar cilindros de corte (furos)
furos = []
for x, y in centros_furos:
    furo = Part.makeCylinder(raio_furo, altura_furo, App.Vector(x, y, 0))
    furos.append(furo)

# Juntar todos os furos em uma só forma para facilitar corte
todos_furos = furos[0]
for f in furos[1:]:
    todos_furos = todos_furos.fuse(f)

# Fazer cortes na placa menor E na placa maior
placa_menor_cortada = placa_menor.cut(todos_furos)
placa_maior_cortada = placa_maior.cut(todos_furos)

# ===== CRIAR OBJETOS NO DOCUMENTO =====
obj_placa_maior = doc.addObject("Part::Feature", "PlacaMaior_95x60")
obj_placa_maior.Shape = placa_maior_cortada

obj_placa_menor = doc.addObject("Part::Feature", "PlacaMenor_92x57_ComFuros")
obj_placa_menor.Shape = placa_menor_cortada

# Aplicar cores diferentes para distinguir as placas
Gui.getDocument("PlacasDuplas").getObject("PlacaMaior_95x60").ViewObject.ShapeColor = (0.8, 0.8, 0.8)  # Cinza claro
Gui.getDocument("PlacasDuplas").getObject("PlacaMenor_92x57_ComFuros").ViewObject.ShapeColor = (0.0, 0.0, 1.0)  # Azul

doc.recompute()