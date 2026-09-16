import pytest
from unittest.mock import MagicMock
from PyQt6.QtCore import QObject
from citadel.presentation.viewmodels.sample_viewmodel import SampleViewModel
from citadel.core.exceptions import UnauthorizedRoleError

class SignalCatcher:
    def __init__(self):
        self.emitted = False
        self.args = None
        
    def catch(self, *args):
        self.emitted = True
        self.args = args

def test_sample_viewmodel_validation_success():
    mock_service = MagicMock()
    mock_service.validate_result.return_value = "VALIDATED_RESULT"
    
    vm = SampleViewModel(mock_service)
    catcher = SignalCatcher()
    vm.result_validated.connect(catcher.catch)
    
    vm.validate_result(1, 1)
    
    assert catcher.emitted is True
    assert catcher.args[0] == "VALIDATED_RESULT"

def test_sample_viewmodel_validation_error():
    mock_service = MagicMock()
    mock_service.validate_result.side_effect = UnauthorizedRoleError("Only Bioanalist can validate")
    
    vm = SampleViewModel(mock_service)
    catcher = SignalCatcher()
    vm.error_occurred.connect(catcher.catch)
    
    vm.validate_result(1, 2)
    
    assert catcher.emitted is True
    assert "Only Bioanalist can validate" in catcher.args[0]
