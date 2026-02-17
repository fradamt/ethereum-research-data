package vm

import (
	"github.com/ethereum/go-ethereum/common"
	"math/big"
)

// Config holds the EVM configuration.
type Config struct {
	MaxCodeSize int
	Debug       bool
}

// Interpreter executes EVM bytecode.
type Interpreter struct {
	evm *EVM
	cfg Config
}

// Runner is implemented by types that can run contracts.
type Runner interface {
	Run(contract *Contract, input []byte) ([]byte, error)
}

// Run executes the given contract.
func (in *Interpreter) Run(contract *Contract, input []byte) ([]byte, error) {
	var (
		op  OpCode
		mem = NewMemory()
	)
	for {
		op = contract.GetOp(in.evm.pc)
		if err := in.execute(op, mem); err != nil {
			return nil, err
		}
	}
	return nil, nil
}

// opAdd performs addition on the top two stack items.
func opAdd(pc *uint64, interpreter *Interpreter, scope *ScopeContext) ([]byte, error) {
	x, y := scope.Stack.pop(), scope.Stack.peek()
	y.Add(&x, y)
	return nil, nil
}

func min(a, b uint64) uint64 {
	if a < b {
		return a
	}
	return b
}
