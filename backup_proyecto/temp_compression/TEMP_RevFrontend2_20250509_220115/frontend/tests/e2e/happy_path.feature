
# happy_path.feature
# Este archivo define un escenario de prueba E2E (end-to-end) básico
# para validar que un usuario puede crear un video cuento sin errores.

Feature: Crear un video cuento exitosamente (Happy Path)

  Como usuario adulto registrado
  Quiero crear un video cuento personalizado
  Para que mi hijo o hija lo disfrute

  Scenario: Usuario crea un video cuento sin errores
    Given el usuario visita la página de inicio
    When hace clic en "Comenzar ahora"
    And completa el formulario de registro
    And inicia sesión con su nueva cuenta
    And crea un perfil infantil
    And responde a todas las preguntas del asistente (nombre, lugar, problema, objeto mágico, final)
    Then debería ver una pantalla de carga
    And luego debería ver el resultado final con el video cuento generado
