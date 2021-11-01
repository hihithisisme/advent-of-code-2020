package day8

type Machine struct {
	accumulator  int
	pointer      int
	instructions []Instruction
}

func NewMachine(instructions []Instruction) *Machine {
	return &Machine{
		accumulator:  0,
		pointer:      0,
		instructions: instructions,
	}
}

func (m *Machine) operate(instruction Instruction) {
	switch instruction.operation {
	case "nop":
		m.nop()
	case "acc":
		m.acc(instruction.value)
	case "jmp":
		m.jmp(instruction.value)
	default:
		panic("invalid instruction")
	}
}

func (m *Machine) nop() {
	m.pointer++
}

func (m *Machine) acc(val int) {
	m.accumulator += val
	m.pointer++
}

func (m *Machine) jmp(val int) {
	m.pointer += val
}

// returns whether the machine still has instructions
func (m *Machine) step() bool {
	if m.pointer == len(m.instructions) {
		return false
	}

	currentInstruction := m.instructions[m.pointer]
	m.operate(currentInstruction)
	return true
}

func (m *Machine) DetectLoop() bool {
	noRepeat := map[int]bool{}
	for {
		if _, exists := noRepeat[m.pointer]; exists {
			return true
		}

		noRepeat[m.pointer] = true
		if !m.step() {
			return false
		}
	}
}
