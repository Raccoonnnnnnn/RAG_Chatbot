import pickle
import matplotlib.pyplot as plt


def edit_chart_pkl(fig):
    # with open('./data/eval2/enhanced_response_analysis.pkl', 'rb') as f:
    #     fig = pickle.load(f)


    # ------- Trục chứa thời gian phản hồi -------
    ax1 = fig.axes[0]  

    # print list label
    for i, annotation in enumerate(ax1.texts):
        print(f"{i}: {annotation.get_text()}, pos={annotation.get_position()}")

    for annotation in ax1.texts:
        if annotation.get_text() == "9.1":
            x, y = annotation.get_position()
            annotation.set_position((x, y + 4))

    for annotation in ax1.texts:
        if annotation.get_text() == "13.9":
            x, y = annotation.get_position()
            annotation.set_position((x, y - 28))  

    for annotation in ax1.texts:
        if annotation.get_text() == "6.1":
            x, y = annotation.get_position()
            annotation.set_position((x, y - 30)) 
            
    for annotation in ax1.texts:
        if annotation.get_text() == "15.6":
            x, y = annotation.get_position()
            annotation.set_position((x, y - 30)) 

    for annotation in ax1.texts:
        if annotation.get_text() == "12.1":
            x, y = annotation.get_position()
            annotation.set_position((x, y + 3))
            
            
    # ------- Trục chứa chất lượng phản hồi -------
    ax2 = fig.axes[1]

    # print list label
    for i, annotation in enumerate(ax2.texts):
        print(f"{i}: {annotation.get_text()}, pos={annotation.get_position()}")

    for annotation in ax2.texts:
        if annotation.get_text() == "64.40":
            x, y = annotation.get_position()
            annotation.set_position((x, y + 5))  

    for annotation in ax2.texts:
        if annotation.get_text() == "67.00":
            x, y = annotation.get_position()
            annotation.set_position((x, y + 3)) 

    for annotation in ax2.texts:
        if annotation.get_text() == "72.18":
            x, y = annotation.get_position()
            annotation.set_position((x, y + 40))

    for annotation in ax2.texts:
        if annotation.get_text() == "75.00":
            x, y = annotation.get_position()
            annotation.set_position((x, y + 3)) 

    for annotation in ax2.texts:
        if annotation.get_text() == "72.80":
            x, y = annotation.get_position()
            annotation.set_position((x, y + 7))


    plt.savefig(f'./data/eval2/enhanced_response_analysis_highres.png', dpi=300, bbox_inches='tight')
    # with open('./data/eval2/enhanced_response_analysis_adjusted.pkl', 'wb') as f:
    #     pickle.dump(fig, f)

    print("✅ Đã chỉnh sửa nhãn thành công và lưu lại ảnh mới.")