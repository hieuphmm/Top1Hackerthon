import google.generativeai as genai #import library
import time
def get_response(prompt): #function to generate question
  genai.configure(api_key="AIzaSyBaVQH1_D8zggcgBPwe4yunpLepCeIimsQ") #use gemini api
  generation_config = {
    "temperature": 0.5,
    "top_p": 0.9,
    "top_k": 40
  }
  #set the safety infor
  safety_settings = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
  ]
  #create a model
  model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)
  #a prompt for asking to generate questions
  print(prompt)
  convo = model.start_chat() #start to chat
  ### question: why these infor in the loop??? maybe it is not optimize
  try:
    convo.send_message(prompt) #ask for the questions
  except:
    time.sleep(5)
    convo.send_message(prompt)
  output = convo.last.text #get the question
  return output #return the question

def choose_option(target, hand):
    prompt = "Chọn 1 câu trong các câu sau: 0. " + hand[0]

    for i in range(1, len(hand)):
        prompt += ", " + str(i) + ". " + hand[i]

    prompt += ". Câu nào là câu phù hợp nhất với câu hỏi được cho: '" + target + "'. Hãy chọn và trả về 1 con số là số thứ tự của câu đã chọn và ghi trên 1 dòng."
    res = get_response(prompt)
    print(res)
    bang_anh_xa = str.maketrans("", "", ".,:!*#()")

    # Áp dụng bảng ánh xạ vào chuỗi để loại bỏ các ký tự đặc biệt
    chuoi_sau_khi_xoa = res.translate(bang_anh_xa)

    # Tách chuỗi thành các từ
    tach_tu = chuoi_sau_khi_xoa.split()

    # Lọc và lấy các số từ danh sách các từ
    so = [tu for tu in tach_tu if tu.isdigit()]

    # Chuyển đổi mảng chứa các chuỗi số thành mảng chứa các số nguyên
    mang_so = list(map(int, so))

    ans = 0
    # Kiểm tra mang_so và chọn từ phù hợp
    for i in range(0, len(mang_so)):
        if mang_so[i] >= 0 and mang_so[i] < len(hand):
            ans = mang_so[i]
            break
    print(ans)
    return ans

hand = [""]