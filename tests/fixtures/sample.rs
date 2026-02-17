use std::collections::HashMap;
use crate::types::BeaconState;

/// A beacon block header.
pub struct BlockHeader {
    pub slot: u64,
    pub proposer_index: u64,
    pub parent_root: [u8; 32],
}

/// Errors during block processing.
pub enum ProcessingError {
    InvalidHeader,
    InvalidSignature,
    MissingValidator(u64),
}

/// Process state transitions.
pub trait StateTransition {
    /// Apply a state transition for the given block.
    fn apply(&mut self, block: &BlockHeader) -> Result<(), ProcessingError>;
}

/// Block processor implementation.
impl BlockProcessor {
    /// Create a new block processor.
    pub fn new(state: BeaconState) -> Self {
        Self { state }
    }

    /// Process a single block.
    pub fn process_block(&mut self, block: &BlockHeader) -> Result<(), ProcessingError> {
        self.validate(block)?;
        self.state.slot = block.slot;
        Ok(())
    }

    fn validate(&self, block: &BlockHeader) -> Result<(), ProcessingError> {
        if block.slot <= self.state.slot {
            return Err(ProcessingError::InvalidHeader);
        }
        Ok(())
    }
}

fn helper() -> u64 {
    42
}
