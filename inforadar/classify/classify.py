import torch
from transformers import BertTokenizer

from inforadar.classify.bert_classifier import BERTClassifier, get_predictions, create_data_loader


def classify_text(text):
    """ Run multiclass classifier. """

    PRE_TRAINED_MODEL_NAME = 'bert-base-multilingual-cased'
    BATCH_SIZE = 1
    MODE = "text"
    MAX_LENS = {"title": 128, "text": 512, "title_text": 512}
    class_names = {1: 'factual', 2: 'opinion', 3: 'entertainment', 4: 'satire', 5: 'conspiracy'}
    n_classes = 5

    # device = torch.device(type='cuda', index=0)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # Load the BERT tokenizer.
    tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME, do_lower_case=False)

    temp_label = [0]
    test_data_loader = create_data_loader([text], temp_label, tokenizer, MAX_LENS[MODE], BATCH_SIZE)

    # Load saved model
    best_model = BERTClassifier(n_classes)
    best_model.to(device)
    # best_model.load_state_dict(torch.load('inforadar/classify/best_model_state_text.bin'))
    best_model.load_state_dict(
        torch.load('inforadar/classify/best_model_state_text.bin', map_location=torch.device('cpu')))

    # Predicting
    y_article_texts, y_pred, y_pred_probs, y_test = get_predictions(
        best_model,
        test_data_loader,
        device
    )

    y_pred_probs = y_pred_probs.cpu().detach().numpy()[0]
    predictions = {'categories': {cls+1: {'score': y_pred_probs[cls].item()} for cls in range(n_classes)}}
    return predictions

