import matplotlib.pyplot as plt


def edit_chart_pkl3(fig):
    # with open('./data/eval2/enhanced_response_analysis.pkl', 'rb') as f:
    #     fig = pickle.load(f)


    # ------- Trục chứa thời gian phản hồi -------
    ax1 = fig.axes[0]  

    # print list label
    for i, annotation in enumerate(ax1.texts):
        print(f"{i}: {annotation.get_text()}, pos={annotation.get_position()}")

    for annotation in ax1.texts:
        if annotation.get_text() == "10.8":
            x, y = annotation.get_position()
            annotation.set_position((x, y + 4))

        if annotation.get_text() == "15.7":
            x, y = annotation.get_position()
            annotation.set_position((x, y - 30))  
            
        if annotation.get_text() == "16.7":
            x, y = annotation.get_position()
            annotation.set_position((x, y - 30))  
        
        if annotation.get_text() == "19.6":
            x, y = annotation.get_position()
            annotation.set_position((x, y - 30))

        if annotation.get_text() == "22.5":
            x, y = annotation.get_position()
            annotation.set_position((x, y - 30)) 
            
        if annotation.get_text() == "25.8":
            x, y = annotation.get_position()
            annotation.set_position((x, y - 30))
        if annotation.get_text() == "30.7":
            x, y = annotation.get_position()
            annotation.set_position((x, y - 30))
        if annotation.get_text() == "33.5":
            x, y = annotation.get_position()
            annotation.set_position((x, y - 30))
        if annotation.get_text() == "38.9":
            x, y = annotation.get_position()
            annotation.set_position((x, y - 30))
        if annotation.get_text() == "42.1":
            x, y = annotation.get_position()
            annotation.set_position((x, y - 30))
        if annotation.get_text() == "47.9":
            x, y = annotation.get_position()
            annotation.set_position((x, y - 30))
        if annotation.get_text() == "51.7":
            x, y = annotation.get_position()
            annotation.set_position((x, y - 30))
    
            
            
    # ------- Trục chứa chất lượng phản hồi -------
    ax2 = fig.axes[1]

    # print list label
    for i, annotation in enumerate(ax2.texts):
        print(f"{i}: {annotation.get_text()}, pos={annotation.get_position()}")

    for annotation in ax2.texts:
        if annotation.get_text() == "71.80":
            x, y = annotation.get_position()
            annotation.set_position((x, y + 5))  

        if annotation.get_text() == "75.00":
            x, y = annotation.get_position()
            annotation.set_position((x, y + 35)) 
            
        if annotation.get_text() == "78.03":
            x, y = annotation.get_position()
            annotation.set_position((x, y + 35))
            
        if annotation.get_text() == "77.82":
            x, y = annotation.get_position()
            annotation.set_position((x, y + 35)) 

        if annotation.get_text() == "76.60":
            x, y = annotation.get_position()
            annotation.set_position((x, y + 40))
            
        if annotation.get_text() == "79.60":
            x, y = annotation.get_position()  
            annotation.set_position((x, y + 35))
        if annotation.get_text() == "79.00":
            x, y = annotation.get_position()  
            annotation.set_position((x, y + 35))
        if annotation.get_text() == "79.40":
            x, y = annotation.get_position()  
            annotation.set_position((x, y + 35))
        
        if annotation.get_text() == "84.60":
            x, y = annotation.get_position()  
            annotation.set_position((x, y + 35))
            
        if annotation.get_text() == "85.80":
            x, y = annotation.get_position()  
            annotation.set_position((x, y + 35))
            
        if annotation.get_text() == "83.60":
            x, y = annotation.get_position()  
            annotation.set_position((x, y + 35))
            
        if annotation.get_text() == "80.00":
            x, y = annotation.get_position()  
            annotation.set_position((x, y + 5))


    plt.savefig(f'./data/eval3/enhanced_response_analysis_highres.png', dpi=300, bbox_inches='tight')
    # with open('./data/eval2/enhanced_response_analysis_adjusted.pkl', 'wb') as f:
    #     pickle.dump(fig, f)

    print("✅ Đã chỉnh sửa nhãn thành công và lưu lại ảnh mới.")