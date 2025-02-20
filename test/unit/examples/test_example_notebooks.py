import os
from testbook import testbook

from fmeval.util import project_root


bedrock_example_notebook_path = os.path.join(project_root(__file__), "examples", "run_evaluation_bedrock_model.ipynb")


@testbook(bedrock_example_notebook_path)
def test_bedrock_model_notebook(tb):
    tb.inject(
        """
        from unittest.mock import patch, MagicMock
        from io import StringIO
        from botocore.response import StreamingBody
        mock_bedrock = MagicMock()
        mock_bedrock.get_foundation_model.return_value = {"modelDetails": "test"}
        body_encoded = '{"results": [{"outputText": "text"}]}'
        mock_bedrock.invoke_model.return_value = {"body": StreamingBody(StringIO(body_encoded), len(body_encoded))}
        p1 = patch('boto3.client', return_value=mock_bedrock)
        p1.start()
        mock_algo = MagicMock()
        mock_algo.evaluate.return_value = []
        p2 = patch('fmeval.eval_algorithms.factual_knowledge.FactualKnowledge', return_value=mock_algo)
        p2.start()
        """
    )
    tb.execute()
    tb.inject(
        """
        p1.stop()
        p2.stop()
        """
    )


js_model_example_notebook_path = os.path.join(
    project_root(__file__), "examples", "run_evaluation_jumpstart_model.ipynb"
)


@testbook(js_model_example_notebook_path)
def test_js_model_notebook(tb):
    tb.inject(
        """
        from unittest.mock import patch, MagicMock
        js_model = MagicMock()
        mock_predictor = MagicMock()
        js_model.deploy.return_value = mock_predictor
        p1 = patch('sagemaker.jumpstart.model.JumpStartModel', return_value=js_model)
        p1.start()
        mock_js_model_runner = MagicMock()
        p2 = patch('fmeval.model_runners.sm_jumpstart_model_runner.JumpStartModelRunner', return_value=mock_js_model_runner)
        p2.start()
        mock_algo = MagicMock()
        mock_algo.evaluate.return_value = []
        p3 = patch('fmeval.eval_algorithms.factual_knowledge.FactualKnowledge', return_value=mock_algo)
        p3.start()
        """
    )
    tb.execute()
    tb.inject(
        """
        p1.stop()
        p2.stop()
        p3.stop()
        """
    )


custom_model_chatgpt_example_notebook_path = os.path.join(
    project_root(__file__), "examples", "run_evaluations_custom_model_chat_gpt.ipynb"
)


@testbook(custom_model_chatgpt_example_notebook_path)
def test_custom_model_chat_gpt_notebook(tb):
    tb.inject(
        """
        from unittest.mock import patch, MagicMock, mock_open
        from requests.models import Response
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = str.encode('{"choices": [{"message": {"content": "text"}}]}')
        p1 = patch('requests.request', return_value=mock_response)
        p1.start()
        mock_algo = MagicMock()
        mock_algo.evaluate.return_value = []
        p2 = patch('fmeval.eval.get_eval_algorithm', return_value=mock_algo)
        p2.start()
        p3 = patch('__main__.open', mock_open(read_data=None))
        p3.start()
        p4 = patch('__main__.next', return_value="")
        p4.start()
        """
    )
    tb.execute()
    tb.inject(
        """
        p1.stop()
        p2.stop()
        p3.stop()
        p4.stop()
        """
    )


custom_model_hf_example_notebook_path = os.path.join(
    project_root(__file__), "examples", "run_evaluations_custom_model_hf.ipynb"
)


@testbook(custom_model_hf_example_notebook_path)
def test_custom_model_hf_notebook(tb):
    tb.inject(
        """
        from unittest.mock import patch, MagicMock, mock_open
        import torch
        mock_algo = MagicMock()
        mock_algo.evaluate.return_value = []
        p1 = patch('fmeval.eval.get_eval_algorithm', return_value=mock_algo)
        p1.start()

        mock_model = MagicMock()
        mock_model.generate.return_value = torch.tensor([[50256, 198, 464, 717, 640, 314, 2497, 262, 649, 2196, 286,
            262, 983, 11, 314, 373, 523, 6568, 13, 314, 373, 523, 6568, 284, 766, 262, 649, 2196, 286, 262, 983, 11,
            314]])
        p2 = patch('transformers.AutoModelForCausalLM.from_pretrained', return_value=mock_model)
        p2.start()

        mock_tokenizer = MagicMock()
        mock_tokenizer().to.return_value = {"input_ids": torch.tensor([[23421, 318, 262, 3139, 286, 30]])}
        p3 = patch('transformers.AutoTokenizer.from_pretrained', return_value=mock_tokenizer)
        p3.start()

        p4 = patch('__main__.open', mock_open(read_data='data'))
        p4.start()

        p5 = patch('__main__.next', return_value="")
        p5.start()
        """
    )
    tb.execute()
    tb.inject(
        """
        p1.stop()
        p2.stop()
        p3.stop()
        p4.stop()
        p5.stop()
        """
    )
